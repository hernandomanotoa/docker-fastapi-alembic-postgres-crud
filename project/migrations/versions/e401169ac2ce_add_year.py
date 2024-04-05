"""add year

Revision ID: e401169ac2ce
Revises: 37c2dbd1d5cd
Create Date: 2024-04-03 20:32:58.324468

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = 'e401169ac2ce'
down_revision = '37c2dbd1d5cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('song', sa.Column('year', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_song_year'), 'song', ['year'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_song_year'), table_name='song')
    op.drop_column('song', 'year')
    # ### end Alembic commands ###
