package db;

import dict.Dictionary;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.sql.SQLException;
import java.sql.ResultSetMetaData;



public class DBResult {
	
	private ArrayList<Row> rowList;
	public Row[] rows;
	
	public DBResult(ResultSet resultSet) throws SQLException {
		this.rowList = new ArrayList<Row>();
		
		ResultSetMetaData resMeta;
		resMeta = resultSet.getMetaData();
		int numberOfCols = resMeta.getColumnCount();
		String[] columnNames = new String[numberOfCols];
		
		for (int i = 1; i <= numberOfCols; i++) {
			String columnName = resMeta.getColumnName(i);
			columnNames[i-1] = columnName;  // What is this starting at 1 bullshit?	
		}
		
		while (resultSet.next()) {
			Dictionary row = new Dictionary();
			for (String colName: columnNames) {
				row.set(colName, resultSet.getString(colName));
			}
			
			this.rowList.add(new Row(row));
		}
		
		this.rows = new Row[this.rowList.size()];
		for (int r = 0; r < this.rowList.size(); r ++) {
			this.rows[r] = this.rowList.get(r);
		}
		
		// "Delete" rowList
		this.rowList = null;
	}
}
