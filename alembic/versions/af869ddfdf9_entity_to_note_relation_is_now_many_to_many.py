"""entity to note relation is now many-to-many

Revision ID: af869ddfdf9
Revises: 2f55dc4f199f
Create Date: 2014-04-06 09:20:44.509357

"""

# revision identifiers, used by Alembic.
revision = 'af869ddfdf9'
down_revision = '2f55dc4f199f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'Entity_Notes',
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('note_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['entity_id'], ['Entities.id'], ),
        sa.ForeignKeyConstraint(['note_id'], ['Notes.id'], ),
        sa.PrimaryKeyConstraint('entity_id', 'note_id')
    )
    # before dropping notes entity_id column
    # store all the entity_id values in the secondary table
    op.execute("""
      insert into "Entity_Notes"
      select "Notes".entity_id, "Notes".id
      from "Notes"
      where "Notes".entity_id is not NULL
      and exists(
        select "Entities".id
        from "Entities"
        where "Entities".id = "Notes".entity_id
      )""")

    # now drop the entity_id column
    op.drop_column('Notes', 'entity_id')


def downgrade():
    op.add_column(
        'Notes',
        sa.Column('entity_id', sa.INTEGER(), nullable=True)
    )

    # restore data
    op.execute("""
        UPDATE
           "Notes"
        SET
            entity_id = "Entity_Notes".entity_id
        FROM "Entity_Notes"
        WHERE "Notes".id = "Entity_Notes".note_id
    """)

    op.drop_table('Entity_Notes')
