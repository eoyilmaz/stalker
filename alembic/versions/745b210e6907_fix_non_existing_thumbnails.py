"""Fix none-existing thumbnails.

Revision ID: 745b210e6907
Revises: f2005d1fbadc
Create Date: 2016-06-27 17:52:24.381000
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "745b210e6907"
down_revision = "258985128aff"


def upgrade():
    """Fix SimpleEntities with none-existing thumbnail_id's."""
    op.execute(
        """
        update
          "SimpleEntities"
        set thumbnail_id = NULL
        where
          "SimpleEntities".thumbnail_id is not NULL
          and not exists(
            select
              thum.id
            from "SimpleEntities" as thum
            where thum.id = "SimpleEntities".thumbnail_id
          )
        """
    )


def downgrade():
    """Downgrade the tables."""
    # do nothing
    pass
