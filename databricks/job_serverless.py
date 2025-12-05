from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import NotebookTask, Source, Task

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

active_jobs = w.jobs.list_runs(active_only=True)

active_jobs
