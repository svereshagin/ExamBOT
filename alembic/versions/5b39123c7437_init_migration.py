"""Init migration

Revision ID: 5b39123c7437
Revises: 72b70e96ea88
Create Date: 2025-03-07 21:40:08.002403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b39123c7437'
down_revision: Union[str, None] = '72b70e96ea88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('surname', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.VARCHAR(), nullable=False),
    sa.Column('updated_at', sa.VARCHAR(), nullable=False),
    sa.Column('teacher_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'exams', 'students', ['student_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'exams', type_='foreignkey')
    op.drop_table('students')
    # ### end Alembic commands ###
