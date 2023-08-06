from src.cs_models.aact_database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
)


class MeshHeadingModel(Base):
    __tablename__ = 'mesh_headings'
    __table_args__ = (
        {'schema': 'ctgov'},
    )

    id = Column(Integer, primary_key=True)
    qualifier = Column(String)
    heading = Column(String)
    subcategory = Column(String)

    def __repr__(self):
        return "<MeshHeading(id='{}', qualifier='{}', " \
               "heading='{}', subcategory='{}'>"\
            .format(self.id, self.qualifier, self.heading,
                    self.subcategory)
