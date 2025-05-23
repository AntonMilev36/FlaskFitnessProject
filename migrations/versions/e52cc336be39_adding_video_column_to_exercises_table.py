"""Adding video column to exercises table

Revision ID: e52cc336be39
Revises: 7f838590e6e4
Create Date: 2024-11-09 21:09:50.124644

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e52cc336be39'
down_revision = '7f838590e6e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercises', schema=None) as batch_op:
        batch_op.add_column(sa.Column('video_example', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercises', schema=None) as batch_op:
        batch_op.drop_column('video_example')

    # ### end Alembic commands ###
