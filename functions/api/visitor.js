/**
 * Cloudflare Pages Function: /api/visitor
 * 
 * 基于 Cloudflare KV 的 100% 真实边缘访客计数器。
 * 
 * 环境变量与绑定:
 * - env.VISITOR_KV: Cloudflare KV 命名空间绑定 (在 Cloudflare Pages 设置中绑定)
 */

export async function onRequest(context) {
  const { request, env } = context;

  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store, no-cache, must-revalidate'
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  const url = new URL(request.url);
  const action = url.searchParams.get('action') || (request.method === 'POST' ? 'hit' : 'get');

  try {
    const kv = env.VISITOR_KV;

    // 1. 如果已绑定 Cloudflare KV (生产边缘环境)
    if (kv) {
      let currentTotalStr = await kv.get('total_visitors');
      let currentTotal = currentTotalStr ? parseInt(currentTotalStr, 10) : 0;

      if (action === 'hit') {
        currentTotal += 1;
        await kv.put('total_visitors', String(currentTotal));
      }

      return new Response(JSON.stringify({
        success: true,
        source: 'cloudflare_kv',
        total: currentTotal,
        visitorId: currentTotal,
        timestamp: Date.now()
      }), { headers: corsHeaders });
    }

    // 2. 本地开发预览环境或未绑定 KV
    return new Response(JSON.stringify({
      success: true,
      source: 'local_dev',
      total: 1,
      visitorId: 1,
      timestamp: Date.now(),
      note: 'KV [VISITOR_KV] not bound. Please bind VISITOR_KV in Cloudflare Pages settings.'
    }), { headers: corsHeaders });

  } catch (err) {
    return new Response(JSON.stringify({
      success: false,
      error: err.message || 'KV Error',
      total: 1,
      visitorId: 1
    }), {
      status: 500,
      headers: corsHeaders
    });
  }
}
