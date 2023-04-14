"""create tables version 1

Revision ID: d38df6ef5e9c
Revises: 876f8cf2ab2c
Create Date: 2023-04-13 13:41:50.524865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd38df6ef5e9c'
down_revision = '876f8cf2ab2c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cards_type',
    sa.Column('idType', sa.UUID(), nullable=False),
    sa.Column('typeName', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('idType'),
    sa.UniqueConstraint('typeName')
    )
    op.create_table('telegram_users',
    sa.Column('chatId', sa.Integer(), nullable=False),
    sa.Column('statusId', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('chatId'),
    sa.UniqueConstraint('chatId')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('firstName', sa.String(), nullable=False),
    sa.Column('lastName', sa.String(), nullable=False),
    sa.Column('patronymic', sa.String(), nullable=True),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('verified', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('verification_code', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login'),
    sa.UniqueConstraint('verification_code')
    )
    op.create_table('balance_circle',
    sa.Column('idBalance', sa.UUID(), nullable=False),
    sa.Column('labelItem', sa.String(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.Column('userId', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idBalance')
    )
    op.create_table('daily_planner',
    sa.Column('idTaskInCard', sa.UUID(), nullable=False),
    sa.Column('dailyTaskName', sa.String(), nullable=False),
    sa.Column('taskStart', sa.Date(), nullable=False),
    sa.Column('taskEnd', sa.Date(), nullable=False),
    sa.Column('taskColor', sa.String(), nullable=False),
    sa.Column('taskStatus', sa.Boolean(), nullable=False),
    sa.Column('userId', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idTaskInCard')
    )
    op.create_table('gantt_tasks',
    sa.Column('idGanttTask', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nameOfTask', sa.String(), nullable=False),
    sa.Column('userId', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idGanttTask'),
    sa.UniqueConstraint('idGanttTask')
    )
    op.create_table('kanban_cards',
    sa.Column('idCard', sa.UUID(), nullable=False),
    sa.Column('typeOfCard', sa.UUID(), nullable=False),
    sa.Column('userId', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['typeOfCard'], ['cards_type.idType'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idCard')
    )
    op.create_table('technics_settings',
    sa.Column('idTechnic', sa.UUID(), nullable=False),
    sa.Column('workTimer', sa.Integer(), nullable=False),
    sa.Column('shortBreak', sa.Integer(), nullable=False),
    sa.Column('longBreak', sa.Integer(), nullable=False),
    sa.Column('countOfCycles', sa.Integer(), nullable=False),
    sa.Column('userId', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idTechnic')
    )
    op.create_table('user_lists',
    sa.Column('idUserList', sa.UUID(), nullable=False),
    sa.Column('nameOfList', sa.String(), nullable=False),
    sa.Column('userId', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idUserList')
    )
    op.create_table('gantt_task_duration',
    sa.Column('idGanttTask', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ganttTaskStart', sa.Date(), nullable=False),
    sa.Column('ganttTaskEnd', sa.Date(), nullable=False),
    sa.Column('projectId', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['projectId'], ['gantt_tasks.idGanttTask'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idGanttTask'),
    sa.UniqueConstraint('idGanttTask')
    )
    op.create_table('task_in_cards',
    sa.Column('idTaskInCard', sa.UUID(), nullable=False),
    sa.Column('cardId', sa.UUID(), nullable=False),
    sa.Column('taskText', sa.String(), nullable=False),
    sa.Column('isDone', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['cardId'], ['kanban_cards.idCard'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idTaskInCard')
    )
    op.create_table('tasks_list',
    sa.Column('idTaskInList', sa.UUID(), nullable=False),
    sa.Column('textOfItem', sa.String(), nullable=False),
    sa.Column('isChecked', sa.Boolean(), nullable=False),
    sa.Column('userListsId', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['userListsId'], ['user_lists.idUserList'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idTaskInList')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks_list')
    op.drop_table('task_in_cards')
    op.drop_table('gantt_task_duration')
    op.drop_table('user_lists')
    op.drop_table('technics_settings')
    op.drop_table('kanban_cards')
    op.drop_table('gantt_tasks')
    op.drop_table('daily_planner')
    op.drop_table('balance_circle')
    op.drop_table('users')
    op.drop_table('telegram_users')
    op.drop_table('cards_type')
    # ### end Alembic commands ###
