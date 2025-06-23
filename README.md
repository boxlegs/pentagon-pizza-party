# Pentagon Pizza Party
impending geopolitical conflict can be predicted via the pentagon pizza index. this tool polls the nearby dominos and notifies you if activity is higher than usual.

### Installation
You can run this yourself - you just need three things!

- Python3
- A GCP Places API key
- A [ntfy.sh](https://ntfy.sh/) server to point to!

Begin by installing the [populartimes](https://github.com/m-wrzr/populartimes/tree/master) package by `m-wzr`. This wraps the Places API, allowing us to cut out most (if not all) of the legwork.

```sh
pip install --upgrade git+https://github.com/m-wrzr/populartimes
```

Then simply clone the repo, populate the `GCP_ACP_KEY` and `NTFY_URL` environment variables through either your `.env` or `.bashrc` file and you're good to go!.

```
git clone https://github.com/boxlegs/pentagonPizzaParty.git
cd pentagon-pizza-party
pip install -r requirements.txt
echo 'GCP_API_KEY=xxx' | tee -a .env
echo 'NTFY_URL=xxx' | tee -a .env
```
### Usage
Now you can enjoy getting ahead of the curve on world events! Keep in mind that the GCP Places API allows **up to 10000** free API calls per month, so be sure to watch your usage if you're running this script on a schedule.

```sh
python3 pentagonPizzaParty.py
```

### To Do
I'm thinking of adding support for more locations (such as Freddie's Beach Bar), as well as tiered notifications based off the severity of activity spikes (urgent, mild etc). 
