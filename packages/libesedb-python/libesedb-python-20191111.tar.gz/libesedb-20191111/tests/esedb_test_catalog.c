/*
 * Library catalog type test program
 *
 * Copyright (C) 2009-2019, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This software is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this software.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <common.h>
#include <file_stream.h>
#include <types.h>

#if defined( HAVE_STDLIB_H ) || defined( WINAPI )
#include <stdlib.h>
#endif

#include "esedb_test_libcerror.h"
#include "esedb_test_libesedb.h"
#include "esedb_test_macros.h"
#include "esedb_test_memory.h"
#include "esedb_test_unused.h"

#include "../libesedb/libesedb_catalog.h"

#if defined( __GNUC__ ) && !defined( LIBESEDB_DLL_IMPORT )

/* Tests the libesedb_catalog_initialize function
 * Returns 1 if successful or 0 if not
 */
int esedb_test_catalog_initialize(
     void )
{
	libcerror_error_t *error        = NULL;
	libesedb_catalog_t *catalog     = NULL;
	int result                      = 0;

#if defined( HAVE_ESEDB_TEST_MEMORY )
	int number_of_malloc_fail_tests = 2;
	int number_of_memset_fail_tests = 1;
	int test_number                 = 0;
#endif

	/* Test regular cases
	 */
	result = libesedb_catalog_initialize(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = libesedb_catalog_free(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = libesedb_catalog_initialize(
	          NULL,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	catalog = (libesedb_catalog_t *) 0x12345678UL;

	result = libesedb_catalog_initialize(
	          &catalog,
	          &error );

	catalog = NULL;

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

#if defined( HAVE_ESEDB_TEST_MEMORY )

	for( test_number = 0;
	     test_number < number_of_malloc_fail_tests;
	     test_number++ )
	{
		/* Test libesedb_catalog_initialize with malloc failing
		 * Test libesedb_catalog_initialize with malloc failing in libcdata_list_initialize
		 */
		esedb_test_malloc_attempts_before_fail = test_number;

		result = libesedb_catalog_initialize(
		          &catalog,
		          &error );

		if( esedb_test_malloc_attempts_before_fail != -1 )
		{
			esedb_test_malloc_attempts_before_fail = -1;

			if( catalog != NULL )
			{
				libesedb_catalog_free(
				 &catalog,
				 NULL );
			}
		}
		else
		{
			ESEDB_TEST_ASSERT_EQUAL_INT(
			 "result",
			 result,
			 -1 );

			ESEDB_TEST_ASSERT_IS_NULL(
			 "catalog",
			 catalog );

			ESEDB_TEST_ASSERT_IS_NOT_NULL(
			 "error",
			 error );

			libcerror_error_free(
			 &error );
		}
	}
	for( test_number = 0;
	     test_number < number_of_memset_fail_tests;
	     test_number++ )
	{
		/* Test libesedb_catalog_initialize with memset failing
		 */
		esedb_test_memset_attempts_before_fail = test_number;

		result = libesedb_catalog_initialize(
		          &catalog,
		          &error );

		if( esedb_test_memset_attempts_before_fail != -1 )
		{
			esedb_test_memset_attempts_before_fail = -1;

			if( catalog != NULL )
			{
				libesedb_catalog_free(
				 &catalog,
				 NULL );
			}
		}
		else
		{
			ESEDB_TEST_ASSERT_EQUAL_INT(
			 "result",
			 result,
			 -1 );

			ESEDB_TEST_ASSERT_IS_NULL(
			 "catalog",
			 catalog );

			ESEDB_TEST_ASSERT_IS_NOT_NULL(
			 "error",
			 error );

			libcerror_error_free(
			 &error );
		}
	}
#endif /* defined( HAVE_ESEDB_TEST_MEMORY ) */

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( catalog != NULL )
	{
		libesedb_catalog_free(
		 &catalog,
		 NULL );
	}
	return( 0 );
}

/* Tests the libesedb_catalog_free function
 * Returns 1 if successful or 0 if not
 */
int esedb_test_catalog_free(
     void )
{
	libcerror_error_t *error = NULL;
	int result               = 0;

	/* Test error cases
	 */
	result = libesedb_catalog_free(
	          NULL,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* Tests the libesedb_catalog_get_number_of_table_definitions function
 * Returns 1 if successful or 0 if not
 */
int esedb_test_catalog_get_number_of_table_definitions(
     void )
{
	libcerror_error_t *error        = NULL;
	libesedb_catalog_t *catalog     = NULL;
	int number_of_table_definitions = 0;
	int result                      = 0;

	/* Initialize test
	 */
	result = libesedb_catalog_initialize(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test regular cases
	 */
	result = libesedb_catalog_get_number_of_table_definitions(
	          catalog,
	          &number_of_table_definitions,
	          &error );

	ESEDB_TEST_ASSERT_NOT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = libesedb_catalog_get_number_of_table_definitions(
	          NULL,
	          &number_of_table_definitions,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libesedb_catalog_get_number_of_table_definitions(
	          catalog,
	          NULL,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Clean up
	 */
	result = libesedb_catalog_free(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( catalog != NULL )
	{
		libesedb_catalog_free(
		 &catalog,
		 NULL );
	}
	return( 0 );
}

/* Tests the libesedb_catalog_get_table_definition_by_index function
 * Returns 1 if successful or 0 if not
 */
int esedb_test_catalog_get_table_definition_by_index(
     void )
{
	libcerror_error_t *error                      = NULL;
	libesedb_catalog_t *catalog                   = NULL;
	libesedb_table_definition_t *table_definition = NULL;
	int result                                    = 0;

	/* Initialize test
	 */
	result = libesedb_catalog_initialize(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test regular cases
	 */

	/* Test error cases
	 */
	result = libesedb_catalog_get_table_definition_by_index(
	          NULL,
	          0,
	          &table_definition,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libesedb_catalog_get_table_definition_by_index(
	          catalog,
	          0,
	          NULL,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Clean up
	 */
	result = libesedb_catalog_free(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( catalog != NULL )
	{
		libesedb_catalog_free(
		 &catalog,
		 NULL );
	}
	return( 0 );
}

/* Tests the libesedb_catalog_get_table_definition_by_name function
 * Returns 1 if successful or 0 if not
 */
int esedb_test_catalog_get_table_definition_by_name(
     void )
{
	libcerror_error_t *error                      = NULL;
	libesedb_catalog_t *catalog                   = NULL;
	libesedb_table_definition_t *table_definition = NULL;
	char *name                                    = "test";
	int result                                    = 0;

	/* Initialize test
	 */
	result = libesedb_catalog_initialize(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test regular cases
	 */

	/* Test error cases
	 */
	result = libesedb_catalog_get_table_definition_by_name(
	          NULL,
	          (uint8_t *) name,
	          4,
	          &table_definition,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libesedb_catalog_get_table_definition_by_name(
	          catalog,
	          NULL,
	          4,
	          &table_definition,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libesedb_catalog_get_table_definition_by_name(
	          catalog,
	          (uint8_t *) name,
	          (size_t) SSIZE_MAX + 1,
	          &table_definition,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libesedb_catalog_get_table_definition_by_name(
	          catalog,
	          (uint8_t *) name,
	          4,
	          NULL,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Clean up
	 */
	result = libesedb_catalog_free(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( catalog != NULL )
	{
		libesedb_catalog_free(
		 &catalog,
		 NULL );
	}
	return( 0 );
}

/* Tests the libesedb_catalog_get_table_definition_by_utf8_name function
 * Returns 1 if successful or 0 if not
 */
int esedb_test_catalog_get_table_definition_by_utf8_name(
     void )
{
	uint8_t utf8_name[ 5 ]                        = { 't', 'e', 's', 't', 0 };
	libcerror_error_t *error                      = NULL;
	libesedb_catalog_t *catalog                   = NULL;
	libesedb_table_definition_t *table_definition = NULL;
	int result                                    = 0;

	/* Initialize test
	 */
	result = libesedb_catalog_initialize(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test regular cases
	 */

	/* Test error cases
	 */
	result = libesedb_catalog_get_table_definition_by_utf8_name(
	          NULL,
	          utf8_name,
	          4,
	          &table_definition,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libesedb_catalog_get_table_definition_by_utf8_name(
	          catalog,
	          NULL,
	          4,
	          &table_definition,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libesedb_catalog_get_table_definition_by_utf8_name(
	          catalog,
	          utf8_name,
	          (size_t) SSIZE_MAX + 1,
	          &table_definition,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libesedb_catalog_get_table_definition_by_utf8_name(
	          catalog,
	          utf8_name,
	          4,
	          NULL,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Clean up
	 */
	result = libesedb_catalog_free(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( catalog != NULL )
	{
		libesedb_catalog_free(
		 &catalog,
		 NULL );
	}
	return( 0 );
}

/* Tests the libesedb_catalog_get_table_definition_by_utf16_name function
 * Returns 1 if successful or 0 if not
 */
int esedb_test_catalog_get_table_definition_by_utf16_name(
     void )
{
	uint16_t utf16_name[ 5 ]                      = { 't', 'e', 's', 't', 0 };
	libcerror_error_t *error                      = NULL;
	libesedb_catalog_t *catalog                   = NULL;
	libesedb_table_definition_t *table_definition = NULL;
	int result                                    = 0;

	/* Initialize test
	 */
	result = libesedb_catalog_initialize(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test regular cases
	 */

	/* Test error cases
	 */
	result = libesedb_catalog_get_table_definition_by_utf16_name(
	          NULL,
	          utf16_name,
	          4,
	          &table_definition,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libesedb_catalog_get_table_definition_by_utf16_name(
	          catalog,
	          NULL,
	          4,
	          &table_definition,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libesedb_catalog_get_table_definition_by_utf16_name(
	          catalog,
	          utf16_name,
	          (size_t) SSIZE_MAX + 1,
	          &table_definition,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libesedb_catalog_get_table_definition_by_utf16_name(
	          catalog,
	          utf16_name,
	          4,
	          NULL,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Clean up
	 */
	result = libesedb_catalog_free(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( catalog != NULL )
	{
		libesedb_catalog_free(
		 &catalog,
		 NULL );
	}
	return( 0 );
}

/* Tests the libesedb_catalog_read_file_io_handle function
 * Returns 1 if successful or 0 if not
 */
int esedb_test_catalog_read_file_io_handle(
     void )
{
	libcerror_error_t *error    = NULL;
	libesedb_catalog_t *catalog = NULL;
	int result                  = 0;

	/* Initialize test
	 */
	result = libesedb_catalog_initialize(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test regular cases
	 */

	/* Test error cases
	 */
	result = libesedb_catalog_read_file_io_handle(
	          NULL,
	          NULL,
	          NULL,
	          0,
	          NULL,
	          NULL,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	ESEDB_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Clean up
	 */
	result = libesedb_catalog_free(
	          &catalog,
	          &error );

	ESEDB_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "catalog",
	 catalog );

	ESEDB_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( catalog != NULL )
	{
		libesedb_catalog_free(
		 &catalog,
		 NULL );
	}
	return( 0 );
}

#endif /* defined( __GNUC__ ) && !defined( LIBESEDB_DLL_IMPORT ) */

/* The main program
 */
#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
int wmain(
     int argc ESEDB_TEST_ATTRIBUTE_UNUSED,
     wchar_t * const argv[] ESEDB_TEST_ATTRIBUTE_UNUSED )
#else
int main(
     int argc ESEDB_TEST_ATTRIBUTE_UNUSED,
     char * const argv[] ESEDB_TEST_ATTRIBUTE_UNUSED )
#endif
{
	ESEDB_TEST_UNREFERENCED_PARAMETER( argc )
	ESEDB_TEST_UNREFERENCED_PARAMETER( argv )

#if defined( __GNUC__ ) && !defined( LIBESEDB_DLL_IMPORT )

	ESEDB_TEST_RUN(
	 "libesedb_catalog_initialize",
	 esedb_test_catalog_initialize );

	ESEDB_TEST_RUN(
	 "libesedb_catalog_free",
	 esedb_test_catalog_free );

	ESEDB_TEST_RUN(
	 "libesedb_catalog_get_number_of_table_definitions",
	 esedb_test_catalog_get_number_of_table_definitions );

	ESEDB_TEST_RUN(
	 "libesedb_catalog_get_table_definition_by_index",
	 esedb_test_catalog_get_table_definition_by_index );

	ESEDB_TEST_RUN(
	 "libesedb_catalog_get_table_definition_by_name",
	 esedb_test_catalog_get_table_definition_by_name );

	ESEDB_TEST_RUN(
	 "libesedb_catalog_get_table_definition_by_utf8_name",
	 esedb_test_catalog_get_table_definition_by_utf8_name );

	ESEDB_TEST_RUN(
	 "libesedb_catalog_get_table_definition_by_utf16_name",
	 esedb_test_catalog_get_table_definition_by_utf16_name );

	ESEDB_TEST_RUN(
	 "libesedb_catalog_read_file_io_handle",
	 esedb_test_catalog_read_file_io_handle );

#endif /* defined( __GNUC__ ) && !defined( LIBESEDB_DLL_IMPORT ) */

	return( EXIT_SUCCESS );

on_error:
	return( EXIT_FAILURE );
}

