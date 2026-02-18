/**
 * Shared utilities for route handlers.
 */

/**
 * Async route wrapper — catches errors and forwards to Express error handler.
 */
function asyncHandler(fn) {
  return (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);
}

/**
 * Build a paginated response envelope.
 */
function paginatedResponse(rows, total, page, pageSize) {
  return {
    results: rows.map((r) => ({ ...r, documentId: r.id })),
    pagination: {
      page,
      pageSize,
      total,
      pageCount: Math.ceil(total / pageSize),
    },
  };
}

/**
 * Parse common pagination query params with safe defaults.
 */
function parsePagination(query, defaultSort = 'created_at:desc') {
  return {
    page: Math.max(1, parseInt(query.page, 10) || 1),
    pageSize: Math.min(100, Math.max(1, parseInt(query.pageSize, 10) || 25)),
    sort: query.sort || defaultSort,
    search: (query._q || '').trim(),
  };
}

/**
 * Build a safe ORDER BY clause from "field:dir" string.
 */
function safeOrderBy(sort, allowedFields) {
  const [field, dir] = (sort || '').split(':');
  const safeField = allowedFields.includes(field) ? field : allowedFields[0];
  const safeDir = dir?.toLowerCase() === 'asc' ? 'ASC' : 'DESC';
  return `${safeField} ${safeDir}`;
}

module.exports = { asyncHandler, paginatedResponse, parsePagination, safeOrderBy };
