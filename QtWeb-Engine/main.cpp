#include <QApplication>
#include <QWebEngineView>
#include <QSize>
#include <QIcon>
#include <QDropEvent>
#include <QMimeData>

class WebView : public QWebEngineView
{
public:
  WebView() : QWebEngineView()
  {
    
  }
  void dropEvent(QDropEvent* event)
  {
    const QMimeData* mimeData = event->mimeData();
    if (mimeData->hasUrls()) {
      const QList<QUrl> urls = mimeData->urls();
      const QUrl url = urls.front();
      setUrl(url);
    }
  }
};

int main(int argc, char *argv[])
{
  QCoreApplication::setOrganizationName("zerhacken");
  QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
  
  QApplication app(argc, argv);
  QWebEngineView view;  
  const QSize size(960, 720);
  view.resize(size);
  view.show();

  return app.exec();
}