/*
 * Library file type test program
 *
 * Copyright (C) 2010-2019, Joachim Metz <joachim.metz@gmail.com>
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
#include <narrow_string.h>
#include <system_string.h>
#include <types.h>
#include <wide_string.h>

#if defined( HAVE_STDLIB_H ) || defined( WINAPI )
#include <stdlib.h>
#endif

#include "qcow_test_functions.h"
#include "qcow_test_getopt.h"
#include "qcow_test_libbfio.h"
#include "qcow_test_libcerror.h"
#include "qcow_test_libqcow.h"
#include "qcow_test_macros.h"
#include "qcow_test_memory.h"
#include "qcow_test_unused.h"

#include "../libqcow/libqcow_file.h"

#if !defined( LIBQCOW_HAVE_BFIO )

LIBQCOW_EXTERN \
int libqcow_check_file_signature_file_io_handle(
     libbfio_handle_t *file_io_handle,
     libcerror_error_t **error );

LIBQCOW_EXTERN \
int libqcow_file_open_file_io_handle(
     libqcow_file_t *file,
     libbfio_handle_t *file_io_handle,
     int access_flags,
     libqcow_error_t **error );

#endif /* !defined( LIBQCOW_HAVE_BFIO ) */

#if defined( HAVE_WIDE_SYSTEM_CHARACTER ) && SIZEOF_WCHAR_T != 2 && SIZEOF_WCHAR_T != 4
#error Unsupported size of wchar_t
#endif

/* Define to make qcow_test_file generate verbose output
#define QCOW_TEST_FILE_VERBOSE
 */

/* Creates and opens a source file
 * Returns 1 if successful or -1 on error
 */
int qcow_test_file_open_source(
     libqcow_file_t **file,
     libbfio_handle_t *file_io_handle,
     const system_character_t *password,
     libcerror_error_t **error )
{
	static char *function = "qcow_test_file_open_source";
	size_t string_length  = 0;
	int result            = 0;

	if( file == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid file.",
		 function );

		return( -1 );
	}
	if( file_io_handle == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid file IO handle.",
		 function );

		return( -1 );
	}
	if( libqcow_file_initialize(
	     file,
	     error ) != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_INITIALIZE_FAILED,
		 "%s: unable to initialize file.",
		 function );

		goto on_error;
	}
	if( password != NULL )
	{
		string_length = system_string_length(
		                 password );

#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
		result = libqcow_file_set_utf16_password(
		          *file,
		          (uint16_t *) password,
		          string_length,
		          error );
#else
		result = libqcow_file_set_utf8_password(
		          *file,
		          (uint8_t *) password,
		          string_length,
		          error );
#endif
		if( result != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_SET_FAILED,
			 "%s: unable to set password.",
			 function );

			goto on_error;
		}
	}
	result = libqcow_file_open_file_io_handle(
	          *file,
	          file_io_handle,
	          LIBQCOW_OPEN_READ,
	          error );

	if( result != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_IO,
		 LIBCERROR_IO_ERROR_OPEN_FAILED,
		 "%s: unable to open file.",
		 function );

		goto on_error;
	}
	return( 1 );

on_error:
	if( *file != NULL )
	{
		libqcow_file_free(
		 file,
		 NULL );
	}
	return( -1 );
}

/* Closes and frees a source file
 * Returns 1 if successful or -1 on error
 */
int qcow_test_file_close_source(
     libqcow_file_t **file,
     libcerror_error_t **error )
{
	static char *function = "qcow_test_file_close_source";
	int result            = 0;

	if( file == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid file.",
		 function );

		return( -1 );
	}
	if( libqcow_file_close(
	     *file,
	     error ) != 0 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_IO,
		 LIBCERROR_IO_ERROR_CLOSE_FAILED,
		 "%s: unable to close file.",
		 function );

		result = -1;
	}
	if( libqcow_file_free(
	     file,
	     error ) != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_FINALIZE_FAILED,
		 "%s: unable to free file.",
		 function );

		result = -1;
	}
	return( result );
}

/* Tests the libqcow_file_initialize function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_initialize(
     void )
{
	libcerror_error_t *error        = NULL;
	libqcow_file_t *file            = NULL;
	int result                      = 0;

#if defined( HAVE_QCOW_TEST_MEMORY )
	int number_of_malloc_fail_tests = 1;
	int number_of_memset_fail_tests = 1;
	int test_number                 = 0;
#endif

	/* Test regular cases
	 */
	result = libqcow_file_initialize(
	          &file,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "file",
	 file );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = libqcow_file_free(
	          &file,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "file",
	 file );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = libqcow_file_initialize(
	          NULL,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	file = (libqcow_file_t *) 0x12345678UL;

	result = libqcow_file_initialize(
	          &file,
	          &error );

	file = NULL;

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

#if defined( HAVE_QCOW_TEST_MEMORY )

	for( test_number = 0;
	     test_number < number_of_malloc_fail_tests;
	     test_number++ )
	{
		/* Test libqcow_file_initialize with malloc failing
		 */
		qcow_test_malloc_attempts_before_fail = test_number;

		result = libqcow_file_initialize(
		          &file,
		          &error );

		if( qcow_test_malloc_attempts_before_fail != -1 )
		{
			qcow_test_malloc_attempts_before_fail = -1;

			if( file != NULL )
			{
				libqcow_file_free(
				 &file,
				 NULL );
			}
		}
		else
		{
			QCOW_TEST_ASSERT_EQUAL_INT(
			 "result",
			 result,
			 -1 );

			QCOW_TEST_ASSERT_IS_NULL(
			 "file",
			 file );

			QCOW_TEST_ASSERT_IS_NOT_NULL(
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
		/* Test libqcow_file_initialize with memset failing
		 */
		qcow_test_memset_attempts_before_fail = test_number;

		result = libqcow_file_initialize(
		          &file,
		          &error );

		if( qcow_test_memset_attempts_before_fail != -1 )
		{
			qcow_test_memset_attempts_before_fail = -1;

			if( file != NULL )
			{
				libqcow_file_free(
				 &file,
				 NULL );
			}
		}
		else
		{
			QCOW_TEST_ASSERT_EQUAL_INT(
			 "result",
			 result,
			 -1 );

			QCOW_TEST_ASSERT_IS_NULL(
			 "file",
			 file );

			QCOW_TEST_ASSERT_IS_NOT_NULL(
			 "error",
			 error );

			libcerror_error_free(
			 &error );
		}
	}
#endif /* defined( HAVE_QCOW_TEST_MEMORY ) */

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( file != NULL )
	{
		libqcow_file_free(
		 &file,
		 NULL );
	}
	return( 0 );
}

/* Tests the libqcow_file_free function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_free(
     void )
{
	libcerror_error_t *error = NULL;
	int result               = 0;

	/* Test error cases
	 */
	result = libqcow_file_free(
	          NULL,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
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

/* Tests the libqcow_file_open function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_open(
     const system_character_t *source,
     const system_character_t *password )
{
	char narrow_source[ 256 ];

	libcerror_error_t *error = NULL;
	libqcow_file_t *file     = NULL;
	size_t string_length     = 0;
	int result               = 0;

	/* Initialize test
	 */
	result = qcow_test_get_narrow_source(
	          source,
	          narrow_source,
	          256,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = libqcow_file_initialize(
	          &file,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "file",
	 file );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	if( password != NULL )
	{
		string_length = system_string_length(
		                 password );

#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
		result = libqcow_file_set_utf16_password(
		          file,
		          (uint16_t *) password,
		          string_length,
		          &error );
#else
		result = libqcow_file_set_utf8_password(
		          file,
		          (uint8_t *) password,
		          string_length,
		          &error );
#endif
		QCOW_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

	        QCOW_TEST_ASSERT_IS_NULL(
	         "error",
		 error );
	}
	/* Test open
	 */
	result = libqcow_file_open(
	          file,
	          narrow_source,
	          LIBQCOW_OPEN_READ,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = libqcow_file_open(
	          NULL,
	          narrow_source,
	          LIBQCOW_OPEN_READ,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libqcow_file_open(
	          file,
	          NULL,
	          LIBQCOW_OPEN_READ,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libqcow_file_open(
	          file,
	          narrow_source,
	          -1,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Test open when already opened
	 */
	result = libqcow_file_open(
	          file,
	          narrow_source,
	          LIBQCOW_OPEN_READ,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Clean up
	 */
	result = libqcow_file_free(
	          &file,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "file",
	 file );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( file != NULL )
	{
		libqcow_file_free(
		 &file,
		 NULL );
	}
	return( 0 );
}

#if defined( HAVE_WIDE_CHARACTER_TYPE )

/* Tests the libqcow_file_open_wide function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_open_wide(
     const system_character_t *source,
     const system_character_t *password )
{
	wchar_t wide_source[ 256 ];

	libcerror_error_t *error = NULL;
	libqcow_file_t *file     = NULL;
	size_t string_length     = 0;
	int result               = 0;

	/* Initialize test
	 */
	result = qcow_test_get_wide_source(
	          source,
	          wide_source,
	          256,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = libqcow_file_initialize(
	          &file,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "file",
	 file );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	if( password != NULL )
	{
		string_length = system_string_length(
		                 password );

#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
		result = libqcow_file_set_utf16_password(
		          file,
		          (uint16_t *) password,
		          string_length,
		          &error );
#else
		result = libqcow_file_set_utf8_password(
		          file,
		          (uint8_t *) password,
		          string_length,
		          &error );
#endif
		QCOW_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

	        QCOW_TEST_ASSERT_IS_NULL(
	         "error",
		 error );
	}
	/* Test open
	 */
	result = libqcow_file_open_wide(
	          file,
	          wide_source,
	          LIBQCOW_OPEN_READ,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = libqcow_file_open_wide(
	          NULL,
	          wide_source,
	          LIBQCOW_OPEN_READ,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libqcow_file_open_wide(
	          file,
	          NULL,
	          LIBQCOW_OPEN_READ,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libqcow_file_open_wide(
	          file,
	          wide_source,
	          -1,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Test open when already opened
	 */
	result = libqcow_file_open_wide(
	          file,
	          wide_source,
	          LIBQCOW_OPEN_READ,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Clean up
	 */
	result = libqcow_file_free(
	          &file,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "file",
	 file );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( file != NULL )
	{
		libqcow_file_free(
		 &file,
		 NULL );
	}
	return( 0 );
}

#endif /* defined( HAVE_WIDE_CHARACTER_TYPE ) */

/* Tests the libqcow_file_open_file_io_handle function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_open_file_io_handle(
     const system_character_t *source,
     const system_character_t *password )
{
	libbfio_handle_t *file_io_handle = NULL;
	libcerror_error_t *error         = NULL;
	libqcow_file_t *file             = NULL;
	size_t string_length             = 0;
	int result                       = 0;

	/* Initialize test
	 */
	result = libbfio_file_initialize(
	          &file_io_handle,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

        QCOW_TEST_ASSERT_IS_NOT_NULL(
         "file_io_handle",
         file_io_handle );

        QCOW_TEST_ASSERT_IS_NULL(
         "error",
         error );

	string_length = system_string_length(
	                 source );

#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
	result = libbfio_file_set_name_wide(
	          file_io_handle,
	          source,
	          string_length,
	          &error );
#else
	result = libbfio_file_set_name(
	          file_io_handle,
	          source,
	          string_length,
	          &error );
#endif
	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

        QCOW_TEST_ASSERT_IS_NULL(
         "error",
         error );

	result = libqcow_file_initialize(
	          &file,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "file",
	 file );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	if( password != NULL )
	{
		string_length = system_string_length(
		                 password );

#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
		result = libqcow_file_set_utf16_password(
		          file,
		          (uint16_t *) password,
		          string_length,
		          &error );
#else
		result = libqcow_file_set_utf8_password(
		          file,
		          (uint8_t *) password,
		          string_length,
		          &error );
#endif
		QCOW_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

	        QCOW_TEST_ASSERT_IS_NULL(
	         "error",
		 error );
	}
	/* Test open
	 */
	result = libqcow_file_open_file_io_handle(
	          file,
	          file_io_handle,
	          LIBQCOW_OPEN_READ,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = libqcow_file_open_file_io_handle(
	          NULL,
	          file_io_handle,
	          LIBQCOW_OPEN_READ,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libqcow_file_open_file_io_handle(
	          file,
	          NULL,
	          LIBQCOW_OPEN_READ,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = libqcow_file_open_file_io_handle(
	          file,
	          file_io_handle,
	          -1,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Test open when already opened
	 */
	result = libqcow_file_open_file_io_handle(
	          file,
	          file_io_handle,
	          LIBQCOW_OPEN_READ,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Clean up
	 */
	result = libqcow_file_free(
	          &file,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "file",
	 file );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = libbfio_handle_free(
	          &file_io_handle,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
         "file_io_handle",
         file_io_handle );

        QCOW_TEST_ASSERT_IS_NULL(
         "error",
         error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( file != NULL )
	{
		libqcow_file_free(
		 &file,
		 NULL );
	}
	if( file_io_handle != NULL )
	{
		libbfio_handle_free(
		 &file_io_handle,
		 NULL );
	}
	return( 0 );
}

/* Tests the libqcow_file_close function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_close(
     void )
{
	libcerror_error_t *error = NULL;
	int result               = 0;

	/* Test error cases
	 */
	result = libqcow_file_close(
	          NULL,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
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

/* Tests the libqcow_file_open and libqcow_file_close functions
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_open_close(
     const system_character_t *source,
     const system_character_t *password )
{
	libcerror_error_t *error = NULL;
	libqcow_file_t *file     = NULL;
	size_t string_length     = 0;
	int result               = 0;

	/* Initialize test
	 */
	result = libqcow_file_initialize(
	          &file,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "file",
	 file );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	if( password != NULL )
	{
		string_length = system_string_length(
		                 password );

#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
		result = libqcow_file_set_utf16_password(
		          file,
		          (uint16_t *) password,
		          string_length,
		          &error );
#else
		result = libqcow_file_set_utf8_password(
		          file,
		          (uint8_t *) password,
		          string_length,
		          &error );
#endif
		QCOW_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

	        QCOW_TEST_ASSERT_IS_NULL(
	         "error",
		 error );
	}
	/* Test open and close
	 */
#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
	result = libqcow_file_open_wide(
	          file,
	          source,
	          LIBQCOW_OPEN_READ,
	          &error );
#else
	result = libqcow_file_open(
	          file,
	          source,
	          LIBQCOW_OPEN_READ,
	          &error );
#endif

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = libqcow_file_close(
	          file,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 0 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test open and close a second time to validate clean up on close
	 */
#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
	result = libqcow_file_open_wide(
	          file,
	          source,
	          LIBQCOW_OPEN_READ,
	          &error );
#else
	result = libqcow_file_open(
	          file,
	          source,
	          LIBQCOW_OPEN_READ,
	          &error );
#endif

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = libqcow_file_close(
	          file,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 0 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Clean up
	 */
	result = libqcow_file_free(
	          &file,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "file",
	 file );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( file != NULL )
	{
		libqcow_file_free(
		 &file,
		 NULL );
	}
	return( 0 );
}

/* Tests the libqcow_file_signal_abort function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_signal_abort(
     libqcow_file_t *file )
{
	libcerror_error_t *error = NULL;
	int result               = 0;

	/* Test regular cases
	 */
	result = libqcow_file_signal_abort(
	          file,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = libqcow_file_signal_abort(
	          NULL,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
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

/* Tests the libqcow_file_read_buffer function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_read_buffer(
     libqcow_file_t *file )
{
	uint8_t buffer[ 16 ];

	libcerror_error_t *error = NULL;
	size64_t media_size      = 0;
	ssize_t read_count       = 0;
	off64_t offset           = 0;
	int result               = 0;

	/* Determine size
	 */
	result = libqcow_file_get_media_size(
	          file,
	          &media_size,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Reset offset to 0
	 */
	offset = libqcow_file_seek_offset(
	          file,
	          0,
	          SEEK_SET,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT64(
	 "offset",
	 offset,
	 (int64_t) 0 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test regular cases
	 */
	if( media_size > 16 )
	{
		read_count = libqcow_file_read_buffer(
		              file,
		              buffer,
		              16,
		              &error );

		QCOW_TEST_ASSERT_EQUAL_SSIZE(
		 "read_count",
		 read_count,
		 (ssize_t) 16 );

		QCOW_TEST_ASSERT_IS_NULL(
		 "error",
		 error );

		/* Set offset to media_size - 8
		 */
		offset = libqcow_file_seek_offset(
		          file,
		          -8,
		          SEEK_END,
		          &error );

		QCOW_TEST_ASSERT_EQUAL_INT64(
		 "offset",
		 offset,
		 (int64_t) media_size - 8 );

		QCOW_TEST_ASSERT_IS_NULL(
		 "error",
		 error );

		/* Read buffer on media_size boundary
		 */
		read_count = libqcow_file_read_buffer(
		              file,
		              buffer,
		              16,
		              &error );

		QCOW_TEST_ASSERT_EQUAL_SSIZE(
		 "read_count",
		 read_count,
		 (ssize_t) 8 );

		QCOW_TEST_ASSERT_IS_NULL(
		 "error",
		 error );

		/* Read buffer beyond media_size boundary
		 */
		read_count = libqcow_file_read_buffer(
		              file,
		              buffer,
		              16,
		              &error );

		QCOW_TEST_ASSERT_EQUAL_SSIZE(
		 "read_count",
		 read_count,
		 (ssize_t) 0 );

		QCOW_TEST_ASSERT_IS_NULL(
		 "error",
		 error );

		/* Reset offset to 0
		 */
		offset = libqcow_file_seek_offset(
		          file,
		          0,
		          SEEK_SET,
		          &error );

		QCOW_TEST_ASSERT_EQUAL_INT64(
		 "offset",
		 offset,
		 (int64_t) 0 );

		QCOW_TEST_ASSERT_IS_NULL(
		 "error",
		 error );
	}
	/* Test error cases
	 */
	read_count = libqcow_file_read_buffer(
	              NULL,
	              buffer,
	              16,
	              &error );

	QCOW_TEST_ASSERT_EQUAL_SSIZE(
	 "read_count",
	 read_count,
	 (ssize_t) -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	read_count = libqcow_file_read_buffer(
	              file,
	              NULL,
	              16,
	              &error );

	QCOW_TEST_ASSERT_EQUAL_SSIZE(
	 "read_count",
	 read_count,
	 (ssize_t) -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	read_count = libqcow_file_read_buffer(
	              file,
	              buffer,
	              (size_t) SSIZE_MAX + 1,
	              &error );

	QCOW_TEST_ASSERT_EQUAL_SSIZE(
	 "read_count",
	 read_count,
	 (ssize_t) -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
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

/* Tests the libqcow_file_read_buffer_at_offset function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_read_buffer_at_offset(
     libqcow_file_t *file )
{
	uint8_t buffer[ 16 ];

	libcerror_error_t *error = NULL;
	size64_t media_size      = 0;
	ssize_t read_count       = 0;
	int result               = 0;

	/* Determine size
	 */
	result = libqcow_file_get_media_size(
	          file,
	          &media_size,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test regular cases
	 */
	if( media_size > 16 )
	{
		read_count = libqcow_file_read_buffer_at_offset(
		              file,
		              buffer,
		              16,
		              0,
		              &error );

		QCOW_TEST_ASSERT_EQUAL_SSIZE(
		 "read_count",
		 read_count,
		 (ssize_t) 16 );

		QCOW_TEST_ASSERT_IS_NULL(
		 "error",
		 error );

		/* Read buffer on media_size boundary
		 */
		read_count = libqcow_file_read_buffer_at_offset(
		              file,
		              buffer,
		              16,
		              media_size - 8,
		              &error );

		QCOW_TEST_ASSERT_EQUAL_SSIZE(
		 "read_count",
		 read_count,
		 (ssize_t) 8 );

		QCOW_TEST_ASSERT_IS_NULL(
		 "error",
		 error );

		/* Read buffer beyond media_size boundary
		 */
		read_count = libqcow_file_read_buffer_at_offset(
		              file,
		              buffer,
		              16,
		              media_size + 8,
		              &error );

		QCOW_TEST_ASSERT_EQUAL_SSIZE(
		 "read_count",
		 read_count,
		 (ssize_t) 0 );

		QCOW_TEST_ASSERT_IS_NULL(
		 "error",
		 error );
	}
	/* Test error cases
	 */
	read_count = libqcow_file_read_buffer_at_offset(
	              NULL,
	              buffer,
	              16,
	              0,
	              &error );

	QCOW_TEST_ASSERT_EQUAL_SSIZE(
	 "read_count",
	 read_count,
	 (ssize_t) -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	read_count = libqcow_file_read_buffer_at_offset(
	              file,
	              NULL,
	              16,
	              0,
	              &error );

	QCOW_TEST_ASSERT_EQUAL_SSIZE(
	 "read_count",
	 read_count,
	 (ssize_t) -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	read_count = libqcow_file_read_buffer_at_offset(
	              file,
	              buffer,
	              (size_t) SSIZE_MAX + 1,
	              0,
	              &error );

	QCOW_TEST_ASSERT_EQUAL_SSIZE(
	 "read_count",
	 read_count,
	 (ssize_t) -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	read_count = libqcow_file_read_buffer_at_offset(
	              file,
	              buffer,
	              16,
	              -1,
	              &error );

	QCOW_TEST_ASSERT_EQUAL_SSIZE(
	 "read_count",
	 read_count,
	 (ssize_t) -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
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

/* Tests the libqcow_file_seek_offset function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_seek_offset(
     libqcow_file_t *file )
{
	libcerror_error_t *error = NULL;
	size64_t size            = 0;
	off64_t offset           = 0;

	/* Test regular cases
	 */
	offset = libqcow_file_seek_offset(
	          file,
	          0,
	          SEEK_END,
	          &error );

	QCOW_TEST_ASSERT_NOT_EQUAL_INT64(
	 "offset",
	 offset,
	 (int64_t) -1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	size = (size64_t) offset;

	offset = libqcow_file_seek_offset(
	          file,
	          1024,
	          SEEK_SET,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT64(
	 "offset",
	 offset,
	 (int64_t) 1024 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	offset = libqcow_file_seek_offset(
	          file,
	          -512,
	          SEEK_CUR,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT64(
	 "offset",
	 offset,
	 (int64_t) 512 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	offset = libqcow_file_seek_offset(
	          file,
	          (off64_t) ( size + 512 ),
	          SEEK_SET,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT64(
	 "offset",
	 offset,
	 (int64_t) ( size + 512 ) );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Reset offset to 0
	 */
	offset = libqcow_file_seek_offset(
	          file,
	          0,
	          SEEK_SET,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT64(
	 "offset",
	 offset,
	 (int64_t) 0 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	offset = libqcow_file_seek_offset(
	          NULL,
	          0,
	          SEEK_SET,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT64(
	 "offset",
	 offset,
	 (int64_t) -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	offset = libqcow_file_seek_offset(
	          file,
	          -1,
	          SEEK_SET,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT64(
	 "offset",
	 offset,
	 (int64_t) -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	offset = libqcow_file_seek_offset(
	          file,
	          -1,
	          SEEK_CUR,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT64(
	 "offset",
	 offset,
	 (int64_t) -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	offset = libqcow_file_seek_offset(
	          file,
	          (off64_t) ( -1 * ( size + 1 ) ),
	          SEEK_END,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT64(
	 "offset",
	 offset,
	 (int64_t) -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
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

/* Tests the libqcow_file_get_offset function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_get_offset(
     libqcow_file_t *file )
{
	libcerror_error_t *error = NULL;
	off64_t offset           = 0;
	int offset_is_set        = 0;
	int result               = 0;

	/* Test regular cases
	 */
	result = libqcow_file_get_offset(
	          file,
	          &offset,
	          &error );

	QCOW_TEST_ASSERT_NOT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	offset_is_set = result;

	/* Test error cases
	 */
	result = libqcow_file_get_offset(
	          NULL,
	          &offset,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	if( offset_is_set != 0 )
	{
		result = libqcow_file_get_offset(
		          file,
		          NULL,
		          &error );

		QCOW_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		QCOW_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );
	}
	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* Tests the libqcow_file_get_media_size function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_get_media_size(
     libqcow_file_t *file )
{
	libcerror_error_t *error = NULL;
	size64_t media_size      = 0;
	int media_size_is_set    = 0;
	int result               = 0;

	/* Test regular cases
	 */
	result = libqcow_file_get_media_size(
	          file,
	          &media_size,
	          &error );

	QCOW_TEST_ASSERT_NOT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	media_size_is_set = result;

	/* Test error cases
	 */
	result = libqcow_file_get_media_size(
	          NULL,
	          &media_size,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	if( media_size_is_set != 0 )
	{
		result = libqcow_file_get_media_size(
		          file,
		          NULL,
		          &error );

		QCOW_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		QCOW_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );
	}
	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* Tests the libqcow_file_get_format_version function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_get_format_version(
     libqcow_file_t *file )
{
	libcerror_error_t *error  = NULL;
	uint32_t format_version   = 0;
	int format_version_is_set = 0;
	int result                = 0;

	/* Test regular cases
	 */
	result = libqcow_file_get_format_version(
	          file,
	          &format_version,
	          &error );

	QCOW_TEST_ASSERT_NOT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	format_version_is_set = result;

	/* Test error cases
	 */
	result = libqcow_file_get_format_version(
	          NULL,
	          &format_version,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	if( format_version_is_set != 0 )
	{
		result = libqcow_file_get_format_version(
		          file,
		          NULL,
		          &error );

		QCOW_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		QCOW_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );
	}
	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* Tests the libqcow_file_get_encryption_method function
 * Returns 1 if successful or 0 if not
 */
int qcow_test_file_get_encryption_method(
     libqcow_file_t *file )
{
	libcerror_error_t *error     = NULL;
	uint32_t encryption_method   = 0;
	int encryption_method_is_set = 0;
	int result                   = 0;

	/* Test regular cases
	 */
	result = libqcow_file_get_encryption_method(
	          file,
	          &encryption_method,
	          &error );

	QCOW_TEST_ASSERT_NOT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	encryption_method_is_set = result;

	/* Test error cases
	 */
	result = libqcow_file_get_encryption_method(
	          NULL,
	          &encryption_method,
	          &error );

	QCOW_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	QCOW_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	if( encryption_method_is_set != 0 )
	{
		result = libqcow_file_get_encryption_method(
		          file,
		          NULL,
		          &error );

		QCOW_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		QCOW_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );
	}
	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* The main program
 */
#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
int wmain(
     int argc,
     wchar_t * const argv[] )
#else
int main(
     int argc,
     char * const argv[] )
#endif
{
	libbfio_handle_t *file_io_handle    = NULL;
	libcerror_error_t *error            = NULL;
	libqcow_file_t *file                = NULL;
	system_character_t *option_password = NULL;
	system_character_t *source          = NULL;
	system_integer_t option             = 0;
	size_t string_length                = 0;
	int result                          = 0;

	while( ( option = qcow_test_getopt(
	                   argc,
	                   argv,
	                   _SYSTEM_STRING( "p:" ) ) ) != (system_integer_t) -1 )
	{
		switch( option )
		{
			case (system_integer_t) '?':
			default:
				fprintf(
				 stderr,
				 "Invalid argument: %" PRIs_SYSTEM ".\n",
				 argv[ optind - 1 ] );

				return( EXIT_FAILURE );

			case (system_integer_t) 'p':
				option_password = optarg;

				break;
		}
	}
	if( optind < argc )
	{
		source = argv[ optind ];
	}
#if defined( HAVE_DEBUG_OUTPUT ) && defined( QCOW_TEST_FILE_VERBOSE )
	libqcow_notify_set_verbose(
	 1 );
	libqcow_notify_set_stream(
	 stderr,
	 NULL );
#endif

	QCOW_TEST_RUN(
	 "libqcow_file_initialize",
	 qcow_test_file_initialize );

	QCOW_TEST_RUN(
	 "libqcow_file_free",
	 qcow_test_file_free );

#if !defined( __BORLANDC__ ) || ( __BORLANDC__ >= 0x0560 )
	if( source != NULL )
	{
		result = libbfio_file_initialize(
		          &file_io_handle,
		          &error );

		QCOW_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

	        QCOW_TEST_ASSERT_IS_NOT_NULL(
	         "file_io_handle",
	         file_io_handle );

	        QCOW_TEST_ASSERT_IS_NULL(
	         "error",
	         error );

		string_length = system_string_length(
		                 source );

#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
		result = libbfio_file_set_name_wide(
		          file_io_handle,
		          source,
		          string_length,
		          &error );
#else
		result = libbfio_file_set_name(
		          file_io_handle,
		          source,
		          string_length,
		          &error );
#endif
		QCOW_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

	        QCOW_TEST_ASSERT_IS_NULL(
	         "error",
	         error );

		result = libqcow_check_file_signature_file_io_handle(
		          file_io_handle,
		          &error );

		QCOW_TEST_ASSERT_NOT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		QCOW_TEST_ASSERT_IS_NULL(
		 "error",
		 error );
	}
	if( result != 0 )
	{
		QCOW_TEST_RUN_WITH_ARGS(
		 "libqcow_file_open",
		 qcow_test_file_open,
		 source,
		 option_password );

#if defined( HAVE_WIDE_CHARACTER_TYPE )

		QCOW_TEST_RUN_WITH_ARGS(
		 "libqcow_file_open_wide",
		 qcow_test_file_open_wide,
		 source,
		 option_password );

#endif /* defined( HAVE_WIDE_CHARACTER_TYPE ) */

		QCOW_TEST_RUN_WITH_ARGS(
		 "libqcow_file_open_file_io_handle",
		 qcow_test_file_open_file_io_handle,
		 source,
		 option_password );

		QCOW_TEST_RUN(
		 "libqcow_file_close",
		 qcow_test_file_close );

		QCOW_TEST_RUN_WITH_ARGS(
		 "libqcow_file_open_close",
		 qcow_test_file_open_close,
		 source,
		 option_password );

		/* Initialize file for tests
		 */
		result = qcow_test_file_open_source(
		          &file,
		          file_io_handle,
		          option_password,
		          &error );

		QCOW_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

		QCOW_TEST_ASSERT_IS_NOT_NULL(
		 "file",
		 file );

		QCOW_TEST_ASSERT_IS_NULL(
		 "error",
		 error );

		QCOW_TEST_RUN_WITH_ARGS(
		 "libqcow_file_signal_abort",
		 qcow_test_file_signal_abort,
		 file );

		QCOW_TEST_RUN_WITH_ARGS(
		 "libqcow_file_read_buffer",
		 qcow_test_file_read_buffer,
		 file );

		QCOW_TEST_RUN_WITH_ARGS(
		 "libqcow_file_read_buffer_at_offset",
		 qcow_test_file_read_buffer_at_offset,
		 file );

		/* TODO: add tests for libqcow_file_write_buffer */

		/* TODO: add tests for libqcow_file_write_buffer_at_offset */

		QCOW_TEST_RUN_WITH_ARGS(
		 "libqcow_file_seek_offset",
		 qcow_test_file_seek_offset,
		 file );

		QCOW_TEST_RUN_WITH_ARGS(
		 "libqcow_file_get_offset",
		 qcow_test_file_get_offset,
		 file );

		/* TODO: add tests for libqcow_file_set_keys */

		/* TODO: add tests for libqcow_file_set_utf8_password */

		/* TODO: add tests for libqcow_file_set_utf16_password */

		QCOW_TEST_RUN_WITH_ARGS(
		 "libqcow_file_get_media_size",
		 qcow_test_file_get_media_size,
		 file );

		QCOW_TEST_RUN_WITH_ARGS(
		 "libqcow_file_get_format_version",
		 qcow_test_file_get_format_version,
		 file );

		QCOW_TEST_RUN_WITH_ARGS(
		 "libqcow_file_get_encryption_method",
		 qcow_test_file_get_encryption_method,
		 file );

		/* Clean up
		 */
		result = qcow_test_file_close_source(
		          &file,
		          &error );

		QCOW_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 0 );

		QCOW_TEST_ASSERT_IS_NULL(
		 "file",
		 file );

		QCOW_TEST_ASSERT_IS_NULL(
		 "error",
		 error );
	}
	if( file_io_handle != NULL )
	{
		result = libbfio_handle_free(
		          &file_io_handle,
		          &error );

		QCOW_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

		QCOW_TEST_ASSERT_IS_NULL(
	         "file_io_handle",
	         file_io_handle );

	        QCOW_TEST_ASSERT_IS_NULL(
	         "error",
	         error );
	}
#endif /* !defined( __BORLANDC__ ) || ( __BORLANDC__ >= 0x0560 ) */

	return( EXIT_SUCCESS );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( file != NULL )
	{
		libqcow_file_free(
		 &file,
		 NULL );
	}
	if( file_io_handle != NULL )
	{
		libbfio_handle_free(
		 &file_io_handle,
		 NULL );
	}
	return( EXIT_FAILURE );
}

