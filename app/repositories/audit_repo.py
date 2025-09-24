from sqlalchemy.orm import Session
from app.db.models.audit_log import AuditLog

def append(db:Session, actor_id:int, action:str, entity: str, entity_id: int,
           before: str | None, after : str | None) -> AuditLog:
    
    log = AuditLog(actor_id=actor_id, action=action, entity=entity, entity_id=entity_id,
                   before= before, after=after)
    db.add(log); db.commit(); db.refresh(log)
    return log

def list_for_entity(db: Session, entity: str, entity_id : int) -> list[AuditLog]:
    return (db.query(AuditLog)
            .filter(AuditLog.entity ==entity, AuditLog.entity_id==entity_id)
            .order_by(AuditLog.id.desc()).all())


