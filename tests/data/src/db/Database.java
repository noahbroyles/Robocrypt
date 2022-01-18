package db;

import java.sql.*;


public class Database {
	
	private Connection connection;
	
	/***
	 * Creates a new Database object
	 * @param host The ip/hostname of the DB server
	 * @param database The name of the database
	 * @param username The username for the DB login
	 * @param password The password for the DB login
	 */
	public Database(String host, String database, String username, String password) {
		String connectionString;
		connectionString = "jdbc:jtds:sqlserver://" + host + ":1433;"
                + "database=" + database + ";"
                + "user=" + username + ";"
                + "password=" + password + ";"
                + "encrypt=true;"
                + "trustServerCertificate=true;"
                + "loginTimeout=30;";
		
		try {
			this.connection = DriverManager.getConnection(connectionString);
		} catch (SQLException ex) {
			ex.printStackTrace();
		}
	}
	
	
	/***
	 * Performs a query in the Database with no parameters
	 * @param sql The SQL query to run in the database
	 * @return DBResult object containing an array of Row objects
	 */
	public DBResult query(String sql) {
		ResultSet resultSet = null;
		DBResult result = null;
		
		try {
			Statement statement = this.connection.createStatement();
			resultSet = statement.executeQuery(sql);
			result = new DBResult(resultSet);
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		return result;
	}
	
	/***
	 * Performs a query in the database with parameters
	 * @param sql The query to run, with parameters substituted with ?'s
	 * @param params The array of parameters
	 * @return DBResult the results of the query
	 */
	public DBResult query(String sql, Object[] params) {
		ResultSet resultSet = null;
		DBResult result = null;
		
		try {
			
			PreparedStatement prepStmt = this.connection.prepareStatement(sql);
			for (int i = 1; i <= params.length; i++) {
				prepStmt.setObject(i, params[i-1]);
			}
//			Statement statement = this.connection.createStatement();
			resultSet = prepStmt.executeQuery();
			result = new DBResult(resultSet);
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		return result;
	}
	
	
	/***
	 * Closes the database connection
	 */
	public void close() {
		try {
			this.connection.close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}


}
