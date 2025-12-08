from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import Task, NotebookTask, Source
from dotenv import load_dotenv
import os 
import time

load_dotenv()

CLUSTER_ID=os.getenv("CLUSTER_ID")
CLUSTER_NAME=os.getenv("CLUSTER_NAME")

w = WorkspaceClient()

job_name            = 'my-job'
description         = 'run a job'
existing_cluster_id = CLUSTER_ID
notebook_path       = '/DatabricksWorkspace/TomsNotebook.ipynb'
task_key            = 'MyTask'

print("Attempting to create the job. Please wait...\n")

j = w.jobs.create(
  name = job_name,
  tasks = [
    Task(
      description = description,
      existing_cluster_id = CLUSTER_ID,
      notebook_task = NotebookTask(
        base_parameters = dict(""),
        notebook_path = notebook_path,
        source = Source("WORKSPACE")
      ),
      task_key = task_key
    )
  ]
)

print(f"View the job at {w.config.host}/#job/{j.job_id}\n")


job_id = j.job_id

w.jobs.run_now(job_id=job_id)

while True:

  active_jobs = list(w.jobs.list_runs(active_only=True))
  
  if active_jobs:
    for job in active_jobs:
      print(job)
    time.sleep(3)      
  else:
    complete_jobs = list(w.jobs.list_runs(completed_only=True))      
    for job in complete_jobs:
      if job.state.result_state.name == "FAILED" or job.state.life_cycle_state.name == "INTERNAL_ERROR":
        raise Exception(f"Run time was exited\n{job}")
      else:
        print(f'job successful\n{job}')
        w.jobs.delete(job_id=job_id)
        break
