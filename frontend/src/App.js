import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";
import { Layout, Menu } from "antd";
import {
  FileAddOutlined,
  TeamOutlined,
  BarChartOutlined,
} from "@ant-design/icons";
import IngestPage from "./pages/IngestPage";
import PatientsPage from "./pages/PatientsPage";
import AnalyticsPage from "./pages/AnalyticsPage";
import "./App.css";

const { Header, Content } = Layout;

const menuItems = [
  { key: "/", icon: <FileAddOutlined />, label: <Link to="/">Ingest</Link> },
  { key: "/patients", icon: <TeamOutlined />, label: <Link to="/patients">Patients</Link> },
  { key: "/analytics", icon: <BarChartOutlined />, label: <Link to="/analytics">Analytics</Link> },
];

function AppLayout() {
  const location = useLocation();

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header style={{ display: "flex", alignItems: "center" }}>
        <div style={{ color: "#fff", fontSize: 20, fontWeight: "bold", marginRight: 40 }}>
          MediNotes
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[location.pathname]}
          items={menuItems}
          style={{ flex: 1 }}
        />
      </Header>
      <Content style={{ padding: "24px 48px" }}>
        <Routes>
          <Route path="/" element={<IngestPage />} />
          <Route path="/patients" element={<PatientsPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
        </Routes>
      </Content>
    </Layout>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  );
}