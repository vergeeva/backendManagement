"""update tables7

Revision ID: 2e11831b3d60
Revises: 823552d7b6dc
Create Date: 2023-05-24 15:09:40.725417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e11831b3d60'
down_revision = '823552d7b6dc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kanban_cards',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('userId', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task_in_cards',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('kanbanCardId', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['kanbanCardId'], ['kanban_cards.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task_in_cards')
    op.drop_table('kanban_cards')
    # ### end Alembic commands ###
