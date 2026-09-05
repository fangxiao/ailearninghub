/**
 * Cloudflare Pages Function: /api/chat
 * 作为同源 BFF 代理层，在 Cloudflare 边缘节点自动注入 API Key，
 * 彻底杜绝前端代码暴露任何秘钥，同时实现零延迟 SSE 流式回传。
 */

export async function onRequestPost(context) {
  const { request, env } = context;

  // 1. 从 Cloudflare Pages 环境变量中读取安全密钥 (零硬编码，代码库 100% 纯净无密码)
  const apiKey = env.AI_GATEWAY_KEY;
  const targetUrl = env.AI_GATEWAY_URL || 'https://api.ailearning.top/v1/chat/completions';

  if (!apiKey) {
    return new Response(JSON.stringify({ 
      error: '服务配置缺失：请在 Cloudflare Pages 项目后台【设置 - 环境变量】中添加 AI_GATEWAY_KEY。' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  }

  try {
    const requestBody = await request.json();

    // 2. 校验来源安全 (简单防刷)
    const origin = request.headers.get('Origin') || '';
    const referer = request.headers.get('Referer') || '';
    const isAllowedHost = !origin || origin.includes('ailearning.top') || origin.includes('pages.dev') || origin.includes('localhost') || origin.includes('127.0.0.1') || referer.includes('ailearning.top');
    
    if (!isAllowedHost) {
      return new Response(JSON.stringify({ error: 'Forbidden: Invalid request origin' }), {
        status: 403,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // 3. 转发至 Cloudflare Worker AI 网关
    const backendResponse = await fetch(targetUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify(requestBody)
    });

    // 4. 将流式 SSE 响应无缝传回客户端
    return new Response(backendResponse.body, {
      status: backendResponse.status,
      headers: {
        'Content-Type': backendResponse.headers.get('Content-Type') || 'text/event-stream; charset=utf-8',
        'Cache-Control': 'no-cache, no-transform',
        'Connection': 'keep-alive',
        'Access-Control-Allow-Origin': '*'
      }
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message || 'Internal Proxy Error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400'
    }
  });
}
