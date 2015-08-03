knapsack_dir=data/knapsack
coloring_dir=data/coloring
func=dyn_prog
code_dir=./discrete_opt

knapsack: $(knapsack_dir)/out/$(in_name).$(func).out
$(knapsack_dir)/out/$(in_name).$(func).out:
	python $(code_dir)/knapsack.py --input $(knapsack_dir)/in/$(in_name) run $(func) > $@.tmp
	mv $@.tmp $@

knapsack_check: $(knapsack_dir)/out/$(in_name).$(func).out
	python $(code_dir)/knapsack.py --input $(knapsack_dir)/in/$(in_name) --output $^ check $(func)





coloring: $(coloring_dir)/out/$(in_name).out
$(coloring_dir)/out/$(in_name).out:
	eclipse -f $(code_dir)/run.pl -e "main('$(coloring_dir)/in/$(in_name)', '$@')."


sat_coloring:
	python $(code_dir)/coloring.py --graph $(coloring_dir)/in/$(in_name) --soln $(coloring_dir)/out/$(in_name).out --mode 'sat'
