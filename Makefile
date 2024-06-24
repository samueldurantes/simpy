.PHONY: run
run:
	@echo "Running the program..."
	python -m flask --app api.main run
test:
	@echo "Testing the program..."
	python -m unittest discover tests

