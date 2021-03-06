"""empty message

Revision ID: 4256a41d082f
Revises: 
Create Date: 2021-07-16 19:49:04.243558

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '4256a41d082f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('website_link', sa.String(length=120), nullable=True),
    sa.Column('seeking_venue', sa.Boolean(), nullable=True),
    sa.Column('seeking_description', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genres',
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('venues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('website_link', sa.String(length=120), nullable=True),
    sa.Column('seeking_talent', sa.Boolean(), nullable=True),
    sa.Column('seeking_description', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('artist_genres',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['genre'], ['genres.name'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('artist_id', 'genre')
    )
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venue_genres',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['genre'], ['genres.name'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('venue_id', 'genre')
    )
    # ### end Alembic commands ###

    genre_table = table (
        'genres',
        column('name', String)
    )
    genres = [
        {'name': 'Alternative'},
        {'name': 'Blues'},
        {'name': 'Classical'},
        {'name': 'Country'},
        {'name': 'Electronic'},
        {'name': 'Folk'},
        {'name': 'Funk'},
        {'name': 'Hip-Hop'},
        {'name': 'Heavy Metal'},
        {'name': 'Instrumental'},
        {'name': 'Jazz'},
        {'name': 'Musical Theatre'},
        {'name': 'Pop'},
        {'name': 'Punk'},
        {'name': 'R&B'},
        {'name': 'Reggae'},
        {'name': 'Rock n Roll'},
        {'name': 'Soul'},
        {'name': 'Other'},
    ]
    op.bulk_insert(
        genre_table,
        genres
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('venue_genres')
    op.drop_table('shows')
    op.drop_table('artist_genres')
    op.drop_table('venues')
    op.drop_table('genres')
    op.drop_table('artists')
    # ### end Alembic commands ###
