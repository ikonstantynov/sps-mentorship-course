-- Schema routes
CREATE SCHEMA routes;
-- Main table
CREATE TABLE routes.route (
  id varchar(1000) PRIMARY KEY,
  route jsonb NOT NULL,
  version INTEGER NOT NULL DEFAULT 0,
  create_by VARCHAR(100),
  create_date TIMESTAMP,
  modify_by VARCHAR(100),
  modify_date TIMESTAMP
);

-- Index
CREATE UNIQUE INDEX route_unique ON routes.route ((route->'route_id'));
CREATE INDEX route_index ON routes.route USING GIN (route jsonb_path_ops);
CREATE INDEX route_index_search ON routes.route USING GIN ((route->'search') jsonb_path_ops);
CREATE INDEX route_search_create_by ON routes.route (create_by);
CREATE INDEX route_search_modify_by ON routes.route (modify_by);

-- History table
CREATE TABLE routes.route_history (
  action CHAR(1),
  id VARCHAR(1000),
  route jsonb NOT NULL,
  version INTEGER NOT NULL DEFAULT 0,
  create_by VARCHAR(100),
  create_date TIMESTAMP,
  modify_by VARCHAR(100) DEFAULT current_user,
  modify_date TIMESTAMP
);
-- History index
CREATE INDEX route_history_index ON routes.route_history USING GIN (route jsonb_path_ops);
CREATE INDEX route_history_index_search ON routes.route USING GIN ((route->'search') jsonb_path_ops);
CREATE INDEX route_history_search_create_by ON routes.route_history (create_by);
CREATE INDEX route_history_search_modify_by ON routes.route_history (modify_by);


-- Insert and update action

CREATE OR REPLACE FUNCTION process_route_audit() RETURNS TRIGGER AS $route_audit$
  BEGIN

    IF (TG_OP = 'UPDATE') THEN
      NEW.version := (SELECT version FROM routes.route WHERE id=NEW.id) + 1;
      NEW.modify_date := current_timestamp;
      IF NEW.modify_by IS NULL THEN
        NEW.modify_by := current_user;
      END IF;

      INSERT INTO routes.route_history SELECT 'U', OLD.*;
      RETURN NEW;

    ELSIF (TG_OP = 'INSERT') THEN
      NEW.version := 0;
      IF NEW.create_by IS NULL THEN
        NEW.create_by := current_user;
      END IF;
      NEW.create_date := current_timestamp;
      NEW.modify_by := NULL;
      NEW.modify_date := current_timestamp;
      RETURN NEW;
    END IF;
    RETURN NEW;
  END;
$route_audit$ LANGUAGE plpgsql;

-- Delete action
CREATE OR REPLACE FUNCTION delete_route_audit() RETURNS TRIGGER AS $delete_route$
  BEGIN
    OLD.modify_date := current_timestamp;
    OLD.modify_by := current_user;

      INSERT INTO routes.route_history VALUES ('D',  OLD.*);
      RETURN OLD;
  END;
$delete_route$ LANGUAGE plpgsql;


-- Triggers
CREATE TRIGGER route_audit
BEFORE INSERT OR UPDATE ON routes.route
    FOR EACH ROW EXECUTE PROCEDURE process_route_audit();

CREATE TRIGGER delete_route_audit
BEFORE DELETE ON routes.route
    FOR EACH ROW EXECUTE PROCEDURE delete_route_audit();



INSERT INTO routes.route (id, route) VALUES ('as2-to-cvan-receiver-exist', '{"origin": {"s3_object_key": "s3inbtest/incoming*", "s3_bucket": "sps-dev-datastore", "service": "s3_inbound_handler", "mailbox": "test_ABC"}, "route_id": "sps:route::as2-to-cvan-receiver-exist", "steps": [{"action": "delivery", "step_id": "step_00010", "response": {"dynamic_value": "{{context.request.s3_bucket}}", "static_value": "response_incoming"}, "service": "cvan-receiver", "template": {"ObjectUrl": "{{context.request.ObjectUrl}}", "ParentEventId": "{{context.request.ParentEventId}}", "ObjectKey": "{{context.request.ObjectKey}}", "Mailbox": "{{context.request.Mailbox}}"}}]}');


INSERT INTO routes.route (id, route) VALUES ('as2-to-cvan-receiver', '{"route_id":"as2-to-cvan-receiver","origin":{"s3_object_key":"s3inbtest/incoming","s3_bucket":"dev-datastore","service":"s3_inbound_handler"}}');
