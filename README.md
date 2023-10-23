Usage:

1) get API token: https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/

2) setup worklog-jira configuration file for your convenience:
```
cat ~/.config/worklog
{
	"server": "<your_domain>.atlassian.net",
	"email": "<your_username>@<mail_domain>.com",
	"token": "<your_api_key_from_step_1>"
}
```

3) use the util to add a worklog to your jira:
```
./worklog.py -c "<I did something...>" -t "1d" -i "<bug_id>"
```
