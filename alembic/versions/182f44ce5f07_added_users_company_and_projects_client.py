"""added Users.company and Projects.client columns and a new Clients table

Revision ID: 182f44ce5f07
Revises: 59bfe820c369
Create Date: 2014-05-29 11:33:02.313000

"""



# revision identifiers, used by Alembic.
revision = '182f44ce5f07'
down_revision = '59bfe820c369'

from alembic import op
import sqlalchemy as sa

def upgrade():

    # Create Clients table
    op.create_table('Clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Entities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # Create Client_Users table
    op.create_table('Client_Users',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('did', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['did'], ['Clients.id'], ),
    sa.ForeignKeyConstraint(['uid'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('uid', 'did')
    )

    # Create Client_Projects table
    op.create_table('Client_Projects',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('did', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['did'], ['Clients.id'], ),
    sa.ForeignKeyConstraint(['uid'], ['Projects.id'], ),
    sa.PrimaryKeyConstraint('uid', 'did')
    )


    # Users table
    op.add_column('Users', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_foreign_key(name=None, source='Users', referent='Clients', local_cols=['company_id'], remote_cols=['id'])

    # Projects table
    op.add_column('Projects', sa.Column('client_id', sa.Integer(), nullable=True))
    op.create_foreign_key(name=None, source='Projects', referent='Clients', local_cols=['client_id'], remote_cols=['id'])



    '''

    #
    # Original alembic-generated code below
    #

    op.create_table('Clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Entities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('login', sa.String(length=256), nullable=False),
    sa.Column('efficiency', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['Clients.id'], ),
    sa.ForeignKeyConstraint(['id'], ['Entities.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login')
    )


    op.create_table('Projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('lead_id', sa.Integer(), nullable=True),
    sa.Column('repository_id', sa.Integer(), nullable=True),
    sa.Column('structure_id', sa.Integer(), nullable=True),
    sa.Column('image_format_id', sa.Integer(), nullable=True),
    sa.Column('fps', sa.Float(precision=3), nullable=True),
    sa.Column('is_stereoscopic', sa.Boolean(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('status_list_id', sa.Integer(), nullable=False),
    sa.Column('start', sa.DateTime(), nullable=True),
    sa.Column('duration', sa.Interval(), nullable=True),
    sa.Column('computed_end', sa.DateTime(), nullable=True),
    sa.Column('computed_start', sa.DateTime(), nullable=True),
    sa.Column('end', sa.DateTime(), nullable=True),
    sa.Column('code', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['Clients.id'], ),
    sa.ForeignKeyConstraint(['id'], ['Entities.id'], ),
    sa.ForeignKeyConstraint(['image_format_id'], ['ImageFormats.id'], ),
    sa.ForeignKeyConstraint(['lead_id'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['repository_id'], ['Repositories.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['Statuses.id'], ),
    sa.ForeignKeyConstraint(['status_list_id'], ['StatusLists.id'], ),
    sa.ForeignKeyConstraint(['structure_id'], ['Structures.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


    op.create_table('Client_Users',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('did', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['did'], ['Clients.id'], ),
    sa.ForeignKeyConstraint(['uid'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('uid', 'did')
    )


    op.create_table('Client_Projects',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('did', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['did'], ['Clients.id'], ),
    sa.ForeignKeyConstraint(['uid'], ['Projects.id'], ),
    sa.PrimaryKeyConstraint('uid', 'did')
    )
    '''




def downgrade():


    op.drop_constraint(name='users_ibfk_2', type_='foreignkey', table_name='Users')
    op.drop_column('Users', 'company_id')

    op.drop_constraint(name='projects_ibfk_8', type_='foreignkey', table_name='Projects')
    op.drop_column('Projects', 'client_id')

    op.drop_table('Client_Projects')
    op.drop_table('Client_Users')
    op.drop_table('Clients')


    '''

    #
    # Original alembic-generated code below
    #

    op.create_table('projects',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('client_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('lead_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('repository_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('structure_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('image_format_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('fps', mysql.FLOAT(), nullable=True),
    sa.Column('is_stereoscopic', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('status_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('status_list_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('start', mysql.DATETIME(), nullable=True),
    sa.Column('duration', mysql.DATETIME(), nullable=True),
    sa.Column('computed_end', mysql.DATETIME(), nullable=True),
    sa.Column('computed_start', mysql.DATETIME(), nullable=True),
    sa.Column('end', mysql.DATETIME(), nullable=True),
    sa.Column('code', mysql.VARCHAR(length=256), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], [u'clients.id'], name=u'projects_ibfk_2'),
    sa.ForeignKeyConstraint(['id'], [u'entities.id'], name=u'projects_ibfk_1'),
    sa.ForeignKeyConstraint(['image_format_id'], [u'imageformats.id'], name=u'projects_ibfk_6'),
    sa.ForeignKeyConstraint(['lead_id'], [u'users.id'], name=u'projects_ibfk_3'),
    sa.ForeignKeyConstraint(['repository_id'], [u'repositories.id'], name=u'projects_ibfk_4'),
    sa.ForeignKeyConstraint(['status_id'], [u'statuses.id'], name=u'projects_ibfk_7'),
    sa.ForeignKeyConstraint(['status_list_id'], [u'statuslists.id'], name=u'projects_ibfk_8'),
    sa.ForeignKeyConstraint(['structure_id'], [u'structures.id'], name=u'projects_ibfk_5'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )


    op.create_table('client_users',
    sa.Column('uid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('did', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['did'], [u'clients.id'], name=u'client_users_ibfk_2'),
    sa.ForeignKeyConstraint(['uid'], [u'users.id'], name=u'client_users_ibfk_1'),
    sa.PrimaryKeyConstraint('uid', 'did'),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )


    op.create_table('users',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('company_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('email', mysql.VARCHAR(length=256), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=256), nullable=False),
    sa.Column('last_login', mysql.DATETIME(), nullable=True),
    sa.Column('login', mysql.VARCHAR(length=256), nullable=False),
    sa.Column('efficiency', mysql.FLOAT(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], [u'clients.id'], name=u'users_ibfk_2'),
    sa.ForeignKeyConstraint(['id'], [u'entities.id'], name=u'users_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )


    op.create_table('clients',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id'], [u'entities.id'], name=u'clients_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )


    op.create_table('client_projects',
    sa.Column('uid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('did', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['did'], [u'clients.id'], name=u'client_projects_ibfk_2'),
    sa.ForeignKeyConstraint(['uid'], [u'projects.id'], name=u'client_projects_ibfk_1'),
    sa.PrimaryKeyConstraint('uid', 'did'),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )


    op.drop_table('Client_Projects')
    op.drop_table('Client_Users')
    op.drop_table('Clients')

    '''


