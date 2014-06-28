knapsack_dir=data/knapsack
func='dyn_prog'

knapsack: $(knapsack_dir)/out/$(in_name).$(func).out
$(knapsack_dir)/out/$(in_name).$(func).out:
	python knapsack.py --input $(knapsack_dir)/in/$(in_name) run $(func) > $@.tmp
	mv $@.tmp $@

knapsack_check: $(knapsack_dir)/out/$(in_name).out
	python knapsack.py --input $(knapsack_dir)/in/$(in_name) --output $(knapsack_dir)/out/$(in_name).out check

test:
	make in_name=ks_30_0 func=dyn_prog && cat data/knapsack/out/ks_30_0.dyn_prog.out
	make in_name=ks_30_0 func=branch_bound && cat data/knapsack/out/ks_30_0.branch_bound.out
