MERGE INTO target_table AS target
USING source_table AS source
ON target.key_column = source.key_column
WHEN MATCHED THEN
	UPDATE SET
		target.column_1 = source.column_1,
		target.column_2 = source.column_2
WHEN NOT MATCHED THEN
	INSERT (key_column, column_1, column_2)
	VALUES (source.key_column, source.column_1, source.column_2);
