const request = require('supertest');
const app = require('../src/app');
const pool = require('../src/config/db');

describe('Health Check', () => {
    afterAll(async () => {
        await pool.end();
    });

    it('should return 200 OK', async () => {
        const res = await request(app).get('/health');
        expect(res.statusCode).toEqual(200);
        expect(res.body).toHaveProperty('status', 'ok');
    });
});
