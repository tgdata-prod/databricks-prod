from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import NotebookTask, Source, Task
import time



w = WorkspaceClient()

j = w.jobs.create(
  name = "My Serverless Job",
  tasks = [
    Task(
      notebook_task = NotebookTask(
      notebook_path = "/DatabricksWorkspace/TomsNotebook.ipynb",
      source = Source("WORKSPACE")
      ),
      task_key = "MyTask",
  )
  ]
)

job_id = j.job_id

w.jobs.run_now(job_id=job_id)

while True:

  active_jobs = list(w.jobs.list_runs(active_only=True))
  
  if not active_jobs:
      raise Exception('no jobs')

  for job in active_jobs:
    print(job)
    time.sleep(3)        
  
  complete_jobs = list(w.jobs.list_runs(completed_only=True))      
  
  for job in complete_jobs:
    if job.state.result_state.name == "FAILED" or job.state.life_cycle_state.name == "INTERNAL_ERROR":
      raise Exception(f"Run time was exited\n{job}")
    else:
      print(f'job successful\n{job}')
      w.jobs.delete(job_id=job_id)
      break
