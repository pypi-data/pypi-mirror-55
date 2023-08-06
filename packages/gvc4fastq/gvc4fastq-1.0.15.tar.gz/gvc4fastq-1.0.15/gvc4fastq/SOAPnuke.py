from toil.common import Toil
from toil.job import Job
from runner.runner import docker_runner, decorator_wrapt, docker_runner_method

import json
import os
import argparse


class Soapnuke(Job):
    @decorator_wrapt
    def __init__(self, raw_read1, raw_read2, output_path, clean_read1,
                 clean_read2, adapter1, adapter2, image, volumes, *args,
                 **kwargs):

        self.image = image
        self.volumes = volumes
        self.commandList = [
            'SOAPnuke', 'filter', '-n', '0.1', '-q', '0.5', '-l', '12', '-Q',
            '2', '-M', '2', '-T', '6', '-1', raw_read1, '-2', raw_read2, '-C',
            clean_read1, '-D', clean_read2, '-o', output_path, '-f', adapter1,
            '-r', adapter2
        ]
        super(Soapnuke, self).__init__(*args, **kwargs)


    @docker_runner('Soapnuke')
    def run(self, jobStore):
        return self.commandList


def args_parser():
    parser = Job.Runner.getDefaultArgumentParser()
    parser.add_argument('--R1', help="R1 fastq file")
    parser.add_argument('--R2', help="R2 fastq file")
    parser.add_argument('--clean_name1', help="clean R2 fastq")
    parser.add_argument('--clean_name2', help='clean R1 fastq')
    parser.add_argument('--adapter1', help='adapter sequence from fq1')
    parser.add_argument('--adapter2', help='adapter sequence from fq2')
    parser.add_argument('--output_path', help='The output folder')
    parser.add_argument('--volumes', type=argparse.FileType('r'))
    parser.add_argument('--image', help="images name",default=u"soapnuke:1.0")
    return parser.parse_args()


if __name__ == '__main__':
    options = args_parser()
    volumes = json.load(options.volumes)
    start_job = Soapnuke(options.R1, options.R2, options.output_path,
                         options.clean_name1, options.clean_name2,
                         options.adapter1, options.adapter2,unicode(options.image),volumes)
    with Toil(options) as toil:
        if not toil.options.restart:
            toil.start(start_job)
        else:
            toil.restart()
