#!/usr/bin/env python
from job_creator import enabled_jobs

job = enabled_jobs[0]
# job.set_source("fake_path")
job.run()
