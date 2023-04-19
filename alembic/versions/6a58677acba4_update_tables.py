"""update tables

Revision ID: 6a58677acba4
Revises: d38df6ef5e9c
Create Date: 2023-04-19 22:30:47.439885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a58677acba4'
down_revision = 'd38df6ef5e9c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'gantt_task_duration', ['idGanttTask'])
    op.create_unique_constraint(None, 'gantt_tasks', ['idGanttTask'])
    op.add_column('technics_settings', sa.Column('settingsName', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'telegram_users', ['chatId'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'telegram_users', type_='unique')
    op.drop_column('technics_settings', 'settingsName')
    op.drop_constraint(None, 'gantt_tasks', type_='unique')
    op.drop_constraint(None, 'gantt_task_duration', type_='unique')
    # ### end Alembic commands ###
