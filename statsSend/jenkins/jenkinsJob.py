#!/usr/bin/env python3

from reporting.category import Category
from statsSend.jenkins.jenkinsBuild import JenkinsBuild

class JenkinsJob:
    def __init__(self, session, url):
        self.session = session
        self.url = url
        self.builds = []

    @property
    def id(self):
        return '/'.join(self.url.strip('/').split('/job/')[1:])

    #{
    #    "_class": "org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject",
    #    "name": "father",
    #    "url": "http://jk.domain/job/grandfather/job/father/",
    #    "jobs": [
    #        { "name": "deploying", "url": "http://jk.domain/job/grandfather/job/father/job/children/" },
    #        ...
    #    ]
    #}
    #
    # OR
    #
    #{
    #    "_class": "org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject",
    #    "name": "father",
    #    "url": "http://jk.domain/job/grandfather/job/father/",
    #    "builds": [
    #        {
    #            "_class": "org.jenkinsci.plugins.workflow.job.WorkflowRun",
    #            "id": "2",
    #            "url": "http://jk.domain/job/grandfather/job/father/1/",
    #            "timestamp": 1493225323359,
    #            "duration": 30315,
    #            "result": "SUCCESS"
    #        },
    #        ...
    #    ]
    #}
    async def retrieve_buildable_descendants(self):
        url = '{:s}?tree=name,url,jobs[name,url],builds[id,url,result,duration,timestamp]'.format(self.url)
        job_json_dict = await self.session.get_resource_at_once_as_json(url)
        if ('builds' in job_json_dict):
            self.builds.extend(job_json_dict['builds'])
            yield self
        else:
            for child_job_json_dict in job_json_dict['jobs']:
                child_job = JenkinsJob(self.session, child_job_json_dict['url'])
                async for buildable_descendant in child_job.retrieve_buildable_descendants():
                    yield buildable_descendant

    def to_category(self):
        return Category('Jenkins', self.url)

    def retrieve_builds_since_posix_timestamp(self, since_posix_timestamp):
        for build_json_dict in self.builds:
            if (build_json_dict['timestamp'] >= since_posix_timestamp):
                yield JenkinsBuild(self.id, build_json_dict)