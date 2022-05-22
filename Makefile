sync:
	@echo "Syncing django with core"
	@(pdm update core && pdm update djangoapp && pdm sync --clean)

sync-core:
	@echo "Syncing django with core"
	@(pdm update core && pdm sync --clean)

sync-djangoapp:
	@echo "Syncing django with core"
	@(pdm update djangoapp && pdm sync --clean)

python_core:
	@echo "cd __core"
	@cd apps/__core && python

python_django_app:
	@echo "cd django_app"
	@cd apps/django_app && python

#test:
	

#@echo "Syncing django with core"
#@(cd apps/django_app && pdm update core && pdm sync --clean)