"""refactor data model with closure table

Revision ID: 494be0ccedb1
Revises: 
Create Date: 2021-03-06 23:28:33.933729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '494be0ccedb1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
        create table region_hierarchy (
            parent_slug text not null,
            child_slug text not null,
            depth int not null,
            primary key (parent_slug, child_slug),
            foreign key (parent_slug) references regions(slug),
            foreign key (child_slug) references regions(slug)
        );

        -- level 1
        insert into region_hierarchy(parent_slug, child_slug, depth)
        select distinct r1.slug, r1.slug, 0
        from regions r1
            left join regions r2 on r1.slug = r2.parent_slug
            left join regions r3 on r2.slug = r3.parent_slug
        where r1.parent_slug is null;

        -- level 2
        insert into region_hierarchy(parent_slug, child_slug, depth)
        select distinct r2.parent_slug, r2.slug, 1
        from regions r1
            left join regions r2 on r1.slug = r2.parent_slug
            left join regions r3 on r2.slug = r3.parent_slug
        where r1.parent_slug is null;

        insert into region_hierarchy(parent_slug, child_slug, depth)
        select distinct r2.slug, r2.slug, 0
        from regions r1
            left join regions r2 on r1.slug = r2.parent_slug
            left join regions r3 on r2.slug = r3.parent_slug
        where r1.parent_slug is null;

        -- level 3
        insert into region_hierarchy(parent_slug, child_slug, depth)
        select distinct r3.slug, r3.slug, 0
        from regions r1
            left join regions r2 on r1.slug = r2.parent_slug
            left join regions r3 on r2.slug = r3.parent_slug
        where r1.parent_slug is null and not (r3.parent_slug is null or r3.slug is null);

        insert into region_hierarchy(parent_slug, child_slug, depth)
        select distinct r3.parent_slug, r3.slug, 1
        from regions r1
            left join regions r2 on r1.slug = r2.parent_slug
            left join regions r3 on r2.slug = r3.parent_slug
        where r1.parent_slug is null and not (r3.parent_slug is null or r3.slug is null);

        insert into region_hierarchy(parent_slug, child_slug, depth)
        select distinct r2.parent_slug, r3.slug, 2
        from regions r1
            left join regions r2 on r1.slug = r2.parent_slug
            left join regions r3 on r2.slug = r3.parent_slug
        where r1.parent_slug is null and not (r2.parent_slug is null or r3.slug is null);

        alter table regions
        drop column parent_slug
    """)


def downgrade():
    pass
