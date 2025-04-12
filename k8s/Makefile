KUBECTL=kubectl

.PHONY: all redis shortener validator restart-shortener restart-validator \
        delete clean status

# Apply all
all: redis shortener validator

# Apply Redis
redis:
	@echo "...Applying Redis..."
	$(KUBECTL) apply -f redis/

# Apply Shortener
shortener:
	@echo "...Applying Shortener resources..."
	$(KUBECTL) apply -f shortener/

# Apply URL Validator
validator:
	@echo "...Applying URL Validator resources..."
	$(KUBECTL) apply -f url-validator/

# Restart shortener
restart-shortener:
	@echo "...Restarting shortener deployment..."
	$(KUBECTL) rollout restart deployment shortener

# Restart validator
restart-validator:
	@echo "...Restarting validator deployment..."
	$(KUBECTL) rollout restart deployment url-validator

# Delete all
delete:
	@echo "...Deleting all resources..."
	-$(KUBECTL) delete -f url-validator/ || true
	-$(KUBECTL) delete -f shortener/ || true
	-$(KUBECTL) delete -f redis/ || true

# Delete and reapply
clean: delete all

# Status of all
status:
	@echo "Pods:"
	$(KUBECTL) get pods
	@echo "Services:"
	$(KUBECTL) get svc
