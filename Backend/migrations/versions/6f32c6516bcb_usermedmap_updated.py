"""usermedmap updated"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f32c6516bcb'
down_revision = '5c45d0b96add'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user_med_map', schema=None) as batch_op:
        # Drop existing (unnamed) constraints (optional, SQLite won't care much)
        # Just recreate with new named FKs

        # Create named FK for medicine_id
        batch_op.create_foreign_key(
            'fk_user_med_map_medicine_id',
            'medicine',
            ['medicine_id'],
            ['id'],
            ondelete='CASCADE'
        )

        # Create named FK for user_id
        batch_op.create_foreign_key(
            'fk_user_med_map_user_id',
            'users',
            ['user_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('user_med_map', schema=None) as batch_op:
        # Drop named FKs in reverse
        batch_op.drop_constraint('fk_user_med_map_user_id', type_='foreignkey')
        batch_op.drop_constraint('fk_user_med_map_medicine_id', type_='foreignkey')
