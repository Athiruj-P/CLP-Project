db_username = "clp_admin"
db_password = "clp_admin"
db_name = "CLP_DB"
item = {
    "db_host" : "mongodb+srv://"+(db_username)+":"+(db_password)+"@cluster-ap.akjvz.mongodb.net/"+(db_name)+"?retryWrites=true&w=majority",
    "db_name": "CLP_DB",
    "db_col_user" : "clp_user",
    "db_col_unit" : "clp_unit",

    # clp_unit fields
    "fld_un_id" : "un_id",
    "fld_un_name" : "un_name",
    "fld_un_abb_name" : "un_abb_name",

    # clp_user fields
    "fld_user_name" : "user_name",
    "fld_user_password" : "user_password",
    "fld_user_status" : "user_status",
    "fld_user_latest_login" : "user_latest_login",
    "fld_user_LOGIN" : 1,
    "fld_user_LOGOUT" : 0,

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