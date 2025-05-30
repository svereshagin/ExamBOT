"""Init migration

Revision ID: 72b70e96ea88
Revises: 
Create Date: 2025-03-06 09:43:42.157921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72b70e96ea88'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teachers',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('telegram_id', sa.BIGINT(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telegram_id')
    )
    op.create_table('students',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('surname', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.VARCHAR(), nullable=False),
    sa.Column('updated_at', sa.VARCHAR(), nullable=False),
    sa.Column('teacher_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exams',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('mark', sa.INTEGER(), nullable=False),
    sa.Column('turn', sa.INTEGER(), nullable=False),
    sa.Column('examination_paper', sa.INTEGER(), nullable=False),
    sa.Column('tasks', sa.TEXT(), nullable=False),
    sa.Column('student_id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('exams')
    op.drop_table('students')
    op.drop_table('teachers')
    # ### end Alembic commands ###
