# mem_issues: OOM killer issue troubleshooting tool that helps to identify the greediest applications.

### How to use it

- create **Python** virtual environment and insall dependencies:
 - `virtualenv mem_issues`
 - `. ./mem_issues/bin/activate`
 - `pip install -U -r requirements.txt`
- collect data running **collect_data.sh** into some file, eg, **ps.log**
- plot data, eg, `./ps2plot.py ps.log`

You might get something like:

![TOP](/top.png?raw=true "Area Plots stacked and non-stacked of greedy apps")


### Licensing

WTFPL
