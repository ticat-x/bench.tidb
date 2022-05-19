# -*- coding: utf-8 -*-

import sys
sys.path.append('../../../helper/python.helper')
sys.path.append('.')
#sys.path.append('..')

from ticat import Env
from my import my_exe
from strs import to_true
from select_ids import bench_result_select
from select_ids import bench_result_update_ids_to_env

def bench_result():
	workload = sys.argv[2]
	tags = sys.argv[3]
	verb = int(sys.argv[4])
	record_ids = sys.argv[5]
	bench_id = sys.argv[6]
	max_cnt = int(sys.argv[7])

	as_baseline = sys.argv[3].lower()
	as_baseline = as_baseline == 'baseline' or to_true(as_baseline)

	has_filter = len(bench_id) != 0 or len(record_ids) != 0 or len(tags) != 0 or len(workload) != 0

	env = Env()

	color = env.must_get('display.color') == 'true'
	width = int(env.must_get('display.width.max'))

	host = env.must_get('bench.meta.host')
	port = env.must_get('bench.meta.port')
	user = env.must_get('bench.meta.user')
	pp = env.get_ex('bench.meta.pwd', '')
	db = env.must_get('bench.meta.db-name')

	tables = my_exe(host, port, user, pp, db, "SHOW TABLES", 'tab')
	if 'bench_meta' not in tables:
		print('[:(] bench_meta table not found')
		return

	ids = []
	if has_filter:
		ids = bench_result_select(host, port, user, pp, db, bench_id, record_ids, tags, workload, max_cnt)
	baseline_id = env.get_ex('bench.meta.result.baseline-id', '')

	if len(baseline_id) == 0 and len(ids) == 0:
		if has_filter:
			print('[:(] no matched bench results')
			return
		else:
			ids = bench_result_select(host, port, user, pp, db, bench_id, record_ids, tags, workload, max_cnt)

	ok = bench_result_update_ids_to_env(env, ids, as_baseline)
	if not ok:
		sys.exit(-1)

bench_result()
