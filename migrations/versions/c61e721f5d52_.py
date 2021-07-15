"""empty message

Revision ID: c61e721f5d52
Revises: 8b50724bf4d9
Create Date: 2021-07-16 07:08:35.912407

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = 'c61e721f5d52'
down_revision = '8b50724bf4d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('Artist', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('Show', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('Show', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('Venue', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('Venue', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###

    op.execute('UPDATE "Artist" SET created_at = ' + datetime.now().strftime("'%Y-%m-%d %H:%M:%S'") + ' WHERE created_at IS NULL;')
    op.execute('UPDATE "Artist" SET updated_at = ' + datetime.now().strftime("'%Y-%m-%d %H:%M:%S'") + ' WHERE updated_at IS NULL;')
    op.execute('UPDATE "Show" SET created_at = ' + datetime.now().strftime("'%Y-%m-%d %H:%M:%S'") + ' WHERE created_at IS NULL;')
    op.execute('UPDATE "Show" SET updated_at = ' + datetime.now().strftime("'%Y-%m-%d %H:%M:%S'") + ' WHERE updated_at IS NULL;')
    op.execute('UPDATE "Venue" SET created_at = ' + datetime.now().strftime("'%Y-%m-%d %H:%M:%S'") + ' WHERE created_at IS NULL;')
    op.execute('UPDATE "Venue" SET updated_at = ' + datetime.now().strftime("'%Y-%m-%d %H:%M:%S'") + ' WHERE updated_at IS NULL;')

    op.alter_column('Artist', 'created_at', nullable=False)
    op.alter_column('Artist', 'updated_at', nullable=False)
    op.alter_column('Show', 'created_at', nullable=False)
    op.alter_column('Show', 'updated_at', nullable=False)
    op.alter_column('Venue', 'created_at', nullable=False)
    op.alter_column('Venue', 'updated_at', nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'updated_at')
    op.drop_column('Venue', 'created_at')
    op.drop_column('Show', 'updated_at')
    op.drop_column('Show', 'created_at')
    op.drop_column('Artist', 'updated_at')
    op.drop_column('Artist', 'created_at')
    # ### end Alembic commands ###
