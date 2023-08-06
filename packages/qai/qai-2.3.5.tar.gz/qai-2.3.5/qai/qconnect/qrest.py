import math
import multiprocessing
import os
import time
from pathlib import Path

from qai.funq import partial
from qai.issues.add_issues import (add_issues_format_insensitive,
                                   add_issues_format_insensitive_batch)
from qai.issues.logs import get_payload_stats
from qai.qconnect.qremoteconnection import QRemoteConnection
from qai.version import __version__
from sanic import Sanic, response
from sanic.log import logger


def get_cpu_quota_within_docker():
    """
    By default, we use mp.cpu_count()
    HOWEVER, if there are cpu limits in certain paths, we assume those are
    from k8s/docker and override with those values
    """
    cpu_cores = multiprocessing.cpu_count()

    cfs_period = Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us")
    cfs_quota = Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us")

    if cfs_period.exists() and cfs_quota.exists():
        # we are in a linux container with cpu quotas!
        with cfs_period.open("rb") as p, cfs_quota.open("rb") as q:
            p, q = int(p.read()), int(q.read())

            # get the cores allocated by dividing the quota
            # in microseconds by the period in microseconds
            cpu_cores = (
                math.ceil(q / p) if q > 0 and p > 0 else multiprocessing.cpu_count()
            )

    return cpu_cores


async def post_root(self, request):
    json_data = request.json
    try:
        # if it has items it is a dict
        _ = json_data.items()
        # if it is a dict, make it an array
        els = [json_data]
    except AttributeError:
        # can't call .items(), so it's already an array
        els = json_data
    resp_list = []

    if self.batching:
        resp_list = add_issues_format_insensitive_batch(self, els, self.debug)
        return response.json(resp_list)

    for el in els:
        el = add_issues_format_insensitive(self, el, self.debug)
        resp_list.append(el)
    return response.json(resp_list)


async def get_root(self, request):
    try:
        white_lister = self.white_lister
    except AttributeError:
        white_lister = None
    resp_obj = {
        "service": self.category,
        "status": "up",
        "host": self.host,
        "port": self.port,
        "qai_version": __version__,
        "white_lister": str(white_lister),
        "analyzer": str(self.analyzer),
    }
    return response.json(resp_obj)


async def add_start_time(request):
    """Prepend initial time when this request was served."""
    request["start_time"] = time.time()


async def add_perf_stats(request, response):
    """
    Prepend initial time when this request was served.
    Log the access long on each request.
    Log num of segments, sentences, words in payload.
    Log sentence and word speed.
    """
    latency = round((time.time() - request["start_time"]) * 1000)
    n_seg, n_sent, n_word = get_payload_stats(request.json)
    latency_sec = latency / 1000

    try:
        # log how long it takes to process seg/sent
        seg_latency = round(latency_sec / n_seg, 2)
        sent_latency = round(latency_sec / n_sent, 2)

        # how many words per sec
        word_speed = round(n_word / latency_sec, 2)

    except:
        # markers - logging error
        seg_latency = -1
        sent_latency = -1
        word_speed = -1

    logger.info(
        "{method} {url} {status} {latency}ms {reqbytes}reqBytes {resbytes}resBytes {n_seg}segs {n_sent}sents {n_word}words {seg_latency}spSeg {sent_latency}spSent {word_speed}wps".format(
            method=request.method,
            ip=request.ip,
            url=request.url,
            status=response.status,
            latency=latency,
            reqbytes=len(request.body),
            resbytes=len(response.body),
            n_seg=n_seg,
            n_sent=n_sent,
            n_word=n_word,
            seg_latency=seg_latency,
            sent_latency=sent_latency,
            word_speed=word_speed,
        )
    )


class QRest(QRemoteConnection):
    def __init__(
        self,
        analyzer,
        category="",
        white_lister=None,
        host="0.0.0.0",
        port=5000,
        workers=get_cpu_quota_within_docker(),
        config_path=["conf", "config.json"],
        batching=False,
        debug=False,
        verbose=False,
        sentence_token_limit=1024,
        ignore_html=True,
    ):
        self.host = host
        self.port = port
        self.workers = workers
        self.batching = batching
        self.debug = debug
        self.verbose = verbose
        self.sentence_token_limit = sentence_token_limit
        self.ignore_html = ignore_html

        config_file = os.path.join(os.getcwd(), *config_path)

        super().__init__(analyzer, category, white_lister, config_file)

        self.app = Sanic(__name__)

        # Add the request and response middleware
        self.app.request_middleware.append(add_start_time)
        self.app.response_middleware.append(add_perf_stats)

        # Add routes
        # This works, but it is better to make these after instantiating the class
        # that way you don't need partial application... see README
        unary_post_root = partial(post_root, self)
        unary_get_root = partial(get_root, self)
        self.app.add_route(unary_post_root, "/", methods=["POST"])
        self.app.add_route(unary_get_root, "/", methods=["GET"])

    def get_future(self):
        """
        Return a Future (Promise in JS land) that can be put on an event loop
        """
        return self.app.create_server(host=self.host, port=self.port)

    def connect(self):
        """
        Doesn't return, makes a blocking connection
        Only use if you are ONLY using REST
        This is a more robust REST server than get_future makes
        see:
        https://sanic.readthedocs.io/en/latest/sanic/deploying.html#asynchronous-support
        """
        if self.workers > 1:
            print(
                f"grpc, and hence AutoML, only support 1 worker, "
                + f"but you are using {self.workers}"
            )
        return self.app.run(
            host=self.host, access_log=False, port=self.port, workers=self.workers
        )
