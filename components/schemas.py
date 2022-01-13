from flask_marshmallow import Marshmallow

ma = Marshmallow()


class ProjectSchema(ma.Schema):
    """
    Schema
    """

    class Meta:
        fields = (
            'id',
            'name',
            'departments',
            'department_id'
        )


class DepartmentSchema(ma.Schema):
    """
    Schema
    """

    class Meta:
        fields = (
            'id',
            'name',
            'assets',
            'asset_id'
        )


class AssetSchema(ma.Schema):
    """
    Schema
    """

    class Meta:
        fields = (
            'id',
            'name',
        )
