"""Tourly Django Project Package."""
# Optional PyMySQL fallback if mysqlclient C-extension is not compiled on student machine
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
