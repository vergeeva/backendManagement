"""update tables6

Revision ID: f5d42566a905
Revises: 83e154e4054c
Create Date: 2023-05-01 15:52:46.544889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5d42566a905'
down_revision = '83e154e4054c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gantt_tasks',
    sa.Column('idGanttTask', sa.UUID(), nullable=False),
    sa.Column('nameOfTask', sa.String(), nullable=False),
    sa.Column('userId', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idGanttTask')
    )
    op.create_table('gantt_task_duration',
    sa.Column('idGanttDuration', sa.UUID(), nullable=False),
    sa.Column('ganttTaskStart', sa.TIMESTAMP(), nullable=False),
    sa.Column('ganttTaskEnd', sa.TIMESTAMP(), nullable=False),
    sa.Column('ganttTaskId', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['ganttTaskId'], ['gantt_tasks.idGanttTask'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idGanttDuration')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('gantt_task_duration')
    op.drop_table('gantt_tasks')
    # ### end Alembic commands ###
