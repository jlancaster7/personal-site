from typing import Any
from pandas import DataFrame
import dash_ag_grid as dag

def base_ag_grid(
        id: str,
        row_data: DataFrame,
        column_defs: list[dict[str, Any]],
        style: dict[str, Any],
        dash_grid_options: Any = {},
        selected_rows = None
    ) -> dag.AgGrid:
    return dag.AgGrid(
        id=id,
        columnSize='responsiveSizeToFit',
        columnDefs=column_defs,
        rowData=row_data.to_dict('records'),
        enableEnterpriseModules=False,
        style={**style},
        dashGridOptions={**dash_grid_options, "enableCellTextSelection": True},
        selectedRows=[] if selected_rows is None else selected_rows,
        defaultColDef=dict(
            autoHeight=True,
            resizable=True,
            sortable=True
        )
    )