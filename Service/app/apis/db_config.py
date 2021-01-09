db_username = "clp_admin"
db_password = "clp_admin"
db_name = "CLP_DB"
item = {
    "db_host" : "mongodb+srv://"+(db_username)+":"+(db_password)+"@cluster-ap.akjvz.mongodb.net/"+(db_name)+"?retryWrites=true&w=majority",
    "db_name": "CLP_DB",
    "db_col_user" : "clp_user",
    "db_col_unit" : "clp_unit",
    "db_col_box_std" : "clp_box_std",
    "db_col_box" : "clp_box",

    # clp_unit fields
    "fld_un_id" : "un_id",
    "fld_un_name" : "un_name",
    "fld_un_abb_name" : "un_abb_name",

    # clp_user fields
    "fld_user_name" : "user_name",
    "fld_user_password" : "user_password",
    "fld_user_status" : "user_status",
    "fld_user_latest_login" : "user_latest_login",
    "fld_user_planners" : "user_planners",
    "fld_user_LOGIN" : 1,
    "fld_user_LOGOUT" : 0,

    # clp_user [planner] fields
    "fld_pln_name" : "pln_name",
    "fld_pln_width" : "pln_width",
    "fld_pln_height" : "pln_height",
    "fld_pln_depth" : "pln_depth",
    "fld_pln_unit_id" : "pln_unit_id",
    "fld_pln_created_date" : "pln_created_date",
    "fld_pln_latest_updated" : "pln_latest_updated",
    "fld_pln_status" : "pln_status",
    "fld_pln_boxes" : "pln_boxes",
    "fld_pln_ACTIVE" : 1,
    "fld_pln_REMOVE" : 0,

    # clp_box fields
    "fld_box_name" : "box_name",
    "fld_box_width" : "box_width",
    "fld_box_height" : "box_height",
    "fld_box_depth" : "box_depth",
    "fld_box_unit_id" : "box_unit_id",
    "fld_box_quantity" : "box_quantity",
    "fld_box_color_id" : "box_color_id",
    "fld_box_created_date" : "box_created_date",
    "fld_box_latest_updated" : "box_latest_updated",
    "fld_box_status" : "box_status",
    "fld_box_ACTIVE" : 1,
    "fld_box_REMOVE" : 0,

    # clp_color fields
    "fld_color_hex" : "color_hex",

    # clp_box_std fields
    "fld_box_std_name" : "box_std_name",
    "fld_box_std_width" : "box_std_width",
    "fld_box_std_height" : "box_std_height",
    "fld_box_std_depth" : "box_std_depth",
    "fld_box_std_unit_id" : "box_std_unit_id",
    
    # clp_container_std fields
    "fld_con_std_name" : "con_std_name",
    "fld_con_std_width" : "con_std_width",
    "fld_con_std_height" : "con_std_height",
    "fld_con_std_depth" : "con_std_depth",
    "fld_con_std_unit_id" : "con_std_unit_id",

    # clp_unit fields
    "fld_role_id" : "role_id",
    "fld_role_name" : "role_name",

    "db_file_path" : "db_file",
    "ml_path" : "ml_model",
    "ref_path" : "ref_model",

    # Font
    "thai_font_folder" : "thai_font",
    "THSarabunNewBold" : "THSarabunNewBold.ttf",
    
}