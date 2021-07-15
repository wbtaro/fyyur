"""empty message

Revision ID: 726fd2d270e7
Revises: 72c27990fe5f
Create Date: 2021-07-15 16:17:31.472330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '726fd2d270e7'
down_revision = '72c27990fe5f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('artist_genres',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['genre'], ['Genre.name'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('artist_id', 'genre')
    )
    op.add_column('Artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=200), nullable=True))
    op.drop_column('Artist', 'genres')

def downgrade():
    op.add_column('Artist', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'seeking_description')
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Artist', 'website_link')
    op.drop_table('artist_genres')
