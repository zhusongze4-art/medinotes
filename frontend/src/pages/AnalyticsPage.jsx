import { useState, useEffect } from "react";
import { Card, Row, Col, Statistic, Spin, Empty } from "antd";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer,
} from "recharts";
import { getAnalytics } from "../api/client";

export default function AnalyticsPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await getAnalytics();
        setData(res.data);
      } catch {
        setData(null);
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  if (loading) return <Spin style={{ display: "block", marginTop: 100 }} />;
  if (!data) return <Empty description="No analytics data available" />;

  const { age_stats, age_distribution, medication_frequency } = data;

  return (
    <div style={{ maxWidth: 900, margin: "0 auto" }}>
      <h2>Patient Analytics</h2>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card><Statistic title="Total Patients" value={age_stats.total} /></Card>
        </Col>
        <Col span={6}>
          <Card><Statistic title="Min Age" value={age_stats.min_age ?? "N/A"} /></Card>
        </Col>
        <Col span={6}>
          <Card><Statistic title="Max Age" value={age_stats.max_age ?? "N/A"} /></Card>
        </Col>
        <Col span={6}>
          <Card><Statistic title="Avg Age" value={age_stats.avg_age ?? "N/A"} precision={1} /></Card>
        </Col>
      </Row>

      <Card title="Age Distribution" style={{ marginBottom: 24 }}>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={age_distribution}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="group" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="count" fill="#1677ff" />
          </BarChart>
        </ResponsiveContainer>
      </Card>

      <Card title="Medication / Intervention Frequency">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={medication_frequency}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="medication" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="count" fill="#52c41a" />
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </div>
  );
}