"""Adds ondelete param to Cards

Revision ID: 4c919af602e5
Revises: 1b3f164bc45a
Create Date: 2025-01-02 14:51:37.479637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c919af602e5'
down_revision = '1b3f164bc45a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_constraint('card_board_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'board', ['board_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('card_board_id_fkey', 'board', ['board_id'], ['id'])

    # ### end Alembic commands ###
