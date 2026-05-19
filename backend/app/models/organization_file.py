from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.connection import Base


class OrganizationFile(Base):
    __tablename__ = "organization_files"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False
    )

    filename = Column(String, nullable=False)

    file_path = Column(String, nullable=False)

    organization = relationship(
        "Organization",
        back_populates="files"
    )
