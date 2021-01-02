db_username = "clp_admin"
db_password = "clp_admin"
db_name = "CLP_DB"
item = {
    "db_host" : "mongodb+srv://"+(db_username)+":"+(db_password)+"@cluster-ap.akjvz.mongodb.net/"+(db_name)+"?retryWrites=true&w=majority",
    "db_name": "CLP_DB",
    "db_col_user" : "clp_user",
    "db_col_unit" : "clp_unit",
    
    # dpml_ml_model fields
    "fld_mlmo_id" : "mlmo_id",
    "fld_mlmo_name" : "mlmo_name",
    "fld_mlmo_path" : "mlmo_path",
    "fld_mlmo_status" : "mlmo_status",
    "fld_mlmo_status_delete" : 0,
    "fld_mlmo_status_active" : 1,
    "fld_mlmo_status_disable" : 2,
    
    # dpml_ref_model fields
    "fld_remo_id" : "remo_id",
    "fld_remo_name" : "remo_name",
    "fld_remo_width" : "remo_width",
    "fld_remo_height" : "remo_height",
    "fld_remo_path" : "remo_path",
    "fld_remo_unit" : "remo_un_id",
    "fld_remo_status" : "remo_status",
    "fld_remo_status_delete" : 0,
    "fld_remo_status_active" : 1,
    "fld_remo_status_disable" : 2,

    # dpml_unit fields
    "fld_un_id" : "un_id",
    "fld_un_name" : "un_name",
    "fld_un_abb_name" : "un_abb_name",

    # dpml_user fields
    "fld_user_id" : "user_id",
    "fld_user_name" : "user_name",
    "fld_user_password" : "user_password",
    "fld_user_login_status" : "user_login_status",
    "fld_user_role_id" : "user_role_id",
    "fld_user_status_login" : 1,
    "fld_user_status_logout" : 0,

    # dpml_unit fields
    "fld_role_id" : "role_id",
    "fld_role_name" : "role_name",

    "db_file_path" : "db_file",
    "ml_path" : "ml_model",
    "ref_path" : "ref_model",

    # Font
    "thai_font_folder" : "thai_font",
    "THSarabunNewBold" : "THSarabunNewBold.ttf",
    
}